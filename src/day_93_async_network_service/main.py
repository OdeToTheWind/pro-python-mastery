"""Day 93 – Capstone: Simple Async Network Service.

Scenario: a *pub-quiz game server*. Players connect over TCP with a tiny
line protocol (``JOIN``, ``ANSWER``, ``SCORES``, ``QUIT``); questions are
broadcast to everyone, only the first correct answer scores, and a
hand-written HTTP endpoint serves the live scoreboard as JSON – all on
``asyncio`` streams from the standard library, no framework.

Deliverables (syllabus):
* ``asyncio.start_server`` TCP service with one coroutine per client
* A line protocol with validation, broadcast and shared game state
* A minimal HTTP/1.1 endpoint on raw streams (status codes, JSON body)
* Robustness: idle timeouts, line-length limits, graceful shutdown
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "TCP server with a coroutine per client": "QuizServer.handle_client",
    "line protocol commands": "QuizServer.command",
    "broadcast to all players": "QuizServer.broadcast",
    "HTTP scoreboard endpoint": "QuizServer.handle_http",
    "start both listeners": "QuizServer.start",
    "graceful shutdown": "QuizServer.close",
}

MAX_LINE = 256


@dataclass
class Question:
    text: str
    answer: str


@dataclass
class Player:
    name: str
    writer: asyncio.StreamWriter
    score: int = 0


@dataclass
class QuizServer:
    questions: list[Question]
    idle_timeout: float = 30.0
    points: int = 10
    players: dict[str, Player] = field(default_factory=dict)
    current: int = -1
    answered: bool = True
    _servers: list[asyncio.Server] = field(default_factory=list)
    _writers: set[asyncio.StreamWriter] = field(default_factory=set)

    async def start(self, host: str = "127.0.0.1", tcp_port: int = 0, http_port: int = 0) -> tuple[int, int]:
        tcp = await asyncio.start_server(self.handle_client, host, tcp_port, limit=MAX_LINE)
        http = await asyncio.start_server(self.handle_http, host, http_port, limit=4096)
        self._servers = [tcp, http]
        return tcp.sockets[0].getsockname()[1], http.sockets[0].getsockname()[1]

    async def close(self) -> None:
        """Stop accepting, say goodbye to everyone, then close the sockets."""
        for server in self._servers:
            server.close()
        await self.broadcast("BYE server shutting down")
        for writer in list(self._writers):
            writer.close()
        for server in self._servers:
            await server.wait_closed()

    @staticmethod
    async def send(writer: asyncio.StreamWriter, line: str) -> None:
        writer.write((line + "\n").encode())
        await writer.drain()  # back-pressure: wait if the client reads slowly

    async def broadcast(self, line: str) -> None:
        for player in list(self.players.values()):
            try:
                await self.send(player.writer, line)
            except ConnectionError:
                self.players.pop(player.name, None)

    async def ask_next(self) -> bool:
        if self.current + 1 >= len(self.questions):
            await self.broadcast("END " + self.scoreline())
            return False
        self.current += 1
        self.answered = False
        await self.broadcast(f"QUESTION {self.current + 1}: {self.questions[self.current].text}")
        return True

    def scoreline(self) -> str:
        ranked = sorted(self.players.values(), key=lambda p: (-p.score, p.name))
        return " ".join(f"{p.name}={p.score}" for p in ranked) or "(no players)"

    async def command(self, line: str, writer: asyncio.StreamWriter, me: Player | None) -> tuple[str, Player | None]:
        verb, _, arg = line.strip().partition(" ")
        verb, arg = verb.upper(), arg.strip()
        if verb == "JOIN":
            if me:
                return "ERR already joined", me
            if not arg.isalnum() or len(arg) > 16:
                return "ERR name must be 1–16 letters/digits", None
            if arg.lower() in self.players:
                return "ERR name taken", None
            me = self.players[arg.lower()] = Player(arg, writer)
            return f"OK joined as {arg}", me
        if verb == "SCORES":
            return "SCORES " + self.scoreline(), me
        if verb == "ANSWER":
            if me is None:
                return "ERR join first", me
            if self.current < 0:
                return "ERR no question yet", me
            if arg.casefold() != self.questions[self.current].answer.casefold():
                return "WRONG", me
            if self.answered:
                return "TOO LATE", me
            self.answered = True
            me.score += self.points
            await self.broadcast(f"WINNER {me.name}")
            return f"CORRECT +{self.points}", me
        return "ERR unknown command", me

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self._writers.add(writer)
        me: Player | None = None
        try:
            await self.send(writer, "WELCOME to the pub quiz – JOIN <name>")
            while True:
                try:
                    raw = await asyncio.wait_for(reader.readline(), self.idle_timeout)
                except TimeoutError:
                    await self.send(writer, "BYE idle too long")
                    break
                except ValueError:  # the line exceeded ``limit``
                    await self.send(writer, "ERR line too long")
                    break
                if not raw:
                    break  # client closed the connection
                line = raw.decode(errors="replace").strip()
                if line.upper() == "QUIT":
                    await self.send(writer, "BYE")
                    break
                if line:
                    reply, me = await self.command(line, writer, me)
                    await self.send(writer, reply)
        except ConnectionError:
            pass
        finally:
            if me:
                self.players.pop(me.name.lower(), None)
            self._writers.discard(writer)
            writer.close()

    async def handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        body: dict[str, object]
        try:
            request = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 5)
            method, path, _version = request.split(b"\r\n", 1)[0].decode("latin-1").split(" ", 2)
            if method != "GET":
                status, body = "405 Method Not Allowed", {"error": "only GET"}
            elif path == "/scoreboard":
                status, body = "200 OK", {"question": self.current + 1,
                                          "players": {p.name: p.score for p in self.players.values()}}
            elif path == "/health":
                status, body = "200 OK", {"status": "ok"}
            else:
                status, body = "404 Not Found", {"error": f"no route {path}"}
        except (ValueError, TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            status, body = "400 Bad Request", {"error": "malformed request"}
        payload = json.dumps(body).encode()
        writer.write(f"HTTP/1.1 {status}\r\nContent-Type: application/json\r\nContent-Length: {len(payload)}\r\n"
                     "Connection: close\r\n\r\n".encode() + payload)
        await writer.drain()
        writer.close()


async def http_get(port: int, path: str, method: str = "GET") -> tuple[int, dict[str, object]]:
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(f"{method} {path} HTTP/1.1\r\nHost: quiz\r\n\r\n".encode())
    await writer.drain()
    raw = await reader.read()
    writer.close()
    head, _, body = raw.partition(b"\r\n\r\n")
    return int(head.split()[1]), json.loads(body)


async def demo() -> list[str]:
    server = QuizServer([Question("Capital of Portugal?", "Lisbon"), Question("2 ** 5?", "32")])
    tcp_port, http_port = await server.start()
    log: list[str] = []
    clients = {}
    for name in ("Ada", "Linus"):
        reader, writer = await asyncio.open_connection("127.0.0.1", tcp_port)
        await reader.readline()
        writer.write(f"JOIN {name}\n".encode())
        await reader.readline()
        clients[name] = (reader, writer)

    async def say(name: str, line: str, replies: int = 1) -> None:
        reader, writer = clients[name]
        writer.write(f"{line}\n".encode())
        for _ in range(replies):
            log.append(f"{name} <- {(await reader.readline()).decode().strip()}")

    await server.ask_next()
    for name in clients:
        log.append(f"{name} <- {(await clients[name][0].readline()).decode().strip()}")
    await say("Linus", "ANSWER porto")
    await say("Ada", "ANSWER lisbon", replies=2)  # WINNER broadcast + CORRECT
    await clients["Linus"][0].readline()  # Linus also sees the WINNER line
    await say("Linus", "ANSWER Lisbon")
    log.append(f"HTTP {await http_get(http_port, '/scoreboard')}")
    await server.close()
    return log


def main() -> None:
    print("Day 93 – Pub-quiz server (TCP + HTTP on localhost)\n")
    for line in asyncio.run(demo()):
        print(" ", line)


if __name__ == "__main__":
    main()
