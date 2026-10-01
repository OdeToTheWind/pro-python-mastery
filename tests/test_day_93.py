"""Tests for Day 93 – Async Network Service (real sockets on 127.0.0.1)."""

import asyncio

from src.day_93_async_network_service.main import MAX_LINE, Question, QuizServer, http_get, main


class Client:
    def __init__(self, reader, writer):
        self.reader, self.writer = reader, writer

    @classmethod
    async def connect(cls, port, name=None):
        client = cls(*await asyncio.open_connection("127.0.0.1", port))
        assert (await client.recv()).startswith("WELCOME")
        if name:
            assert await client.ask(f"JOIN {name}") == f"OK joined as {name}"
        return client

    async def recv(self):
        return (await asyncio.wait_for(self.reader.readline(), 2)).decode().strip()

    async def ask(self, line):
        self.writer.write(line.encode() + b"\n")
        await self.writer.drain()
        return await self.recv()


def play(scenario, **kwargs):
    async def runner():
        server = QuizServer([Question("Largest planet?", "Jupiter"), Question("H2O?", "water")], **kwargs)
        ports = await server.start()
        try:
            return await scenario(server, *ports)
        finally:
            await server.close()

    return asyncio.run(runner())


def test_join_rules():
    async def scenario(server, tcp, _http):
        ada = await Client.connect(tcp, "Ada")
        other = await Client.connect(tcp)
        return [await other.ask("JOIN ada"), await other.ask("JOIN bad name!"), await ada.ask("JOIN again"),
                await other.ask("ANSWER x"), await ada.ask("ANSWER x"), await ada.ask("dance")]

    assert play(scenario) == ["ERR name taken", "ERR name must be 1–16 letters/digits", "ERR already joined",
                              "ERR join first", "ERR no question yet", "ERR unknown command"]


def test_question_broadcast_and_first_correct_answer_wins():
    async def scenario(server, tcp, _http):
        ada, bob = await Client.connect(tcp, "Ada"), await Client.connect(tcp, "Bob")
        await server.ask_next()
        assert await ada.recv() == await bob.recv() == "QUESTION 1: Largest planet?"
        assert await bob.ask("ANSWER saturn") == "WRONG"
        assert await ada.ask("answer JUPITER") == "WINNER Ada"
        assert await ada.recv() == "CORRECT +10"
        assert await bob.recv() == "WINNER Ada"
        assert await bob.ask("ANSWER jupiter") == "TOO LATE"
        await server.ask_next()
        await ada.recv()
        await server.ask_next()  # no more questions
        await bob.recv()
        return await bob.recv(), await bob.ask("SCORES")

    assert play(scenario) == ("END Ada=10 Bob=0", "SCORES Ada=10 Bob=0")


def test_quit_disconnect_and_scoreboard_cleanup():
    async def scenario(server, tcp, _http):
        ada = await Client.connect(tcp, "Ada")
        bob = await Client.connect(tcp, "Bob")
        assert await ada.ask("QUIT") == "BYE"
        bob.writer.close()
        await asyncio.sleep(0.05)
        return server.scoreline()

    assert play(scenario) == "(no players)"


def test_idle_timeout_and_long_lines():
    async def scenario(server, tcp, _http):
        sleepy = await Client.connect(tcp, "Zed")
        noisy = await Client.connect(tcp)
        noisy.writer.write(b"JOIN " + b"x" * (MAX_LINE * 2) + b"\n")
        return await noisy.recv(), await sleepy.recv()

    assert play(scenario, idle_timeout=0.3) == ("ERR line too long", "BYE idle too long")


def test_http_endpoints():
    async def scenario(server, tcp, http):
        ada = await Client.connect(tcp, "Ada")  # keep the reference: a collected client disconnects
        results = [await http_get(http, "/scoreboard"), await http_get(http, "/health"),
                   await http_get(http, "/admin"), await http_get(http, "/scoreboard", "POST")]
        reader, writer = await asyncio.open_connection("127.0.0.1", http)
        writer.write(b"garbage\r\n\r\n")
        results.append((await reader.read()).split(b"\r\n")[0])
        writer.close()
        ada.writer.close()
        return results

    board, health, missing, post, bad = play(scenario)
    assert board == (200, {"question": 0, "players": {"Ada": 0}}) and health == (200, {"status": "ok"})
    assert missing[0] == 404 and post[0] == 405 and bad == b"HTTP/1.1 400 Bad Request"


def test_shutdown_says_goodbye():
    async def scenario(server, tcp, _http):
        ada = await Client.connect(tcp, "Ada")
        await server.close()
        return await ada.recv()

    assert play(scenario) == "BYE server shutting down"


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Ada <- CORRECT +10" in out and "Linus <- TOO LATE" in out and "'Ada': 10" in out
