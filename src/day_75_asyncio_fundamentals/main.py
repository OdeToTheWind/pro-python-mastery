"""Day 75 – Asyncio Fundamentals.

Scenario: an *airport departures board* that queries several airline status
services at once. Each query mostly waits on the network, so one thread with
an event loop can overlap all of them.

Deliverables (syllabus):
* The event loop (``asyncio.run``, ``get_running_loop``, scheduling callbacks)
* Coroutines and ``async``/``await``
* ``gather`` (concurrent awaiting, ``return_exceptions``)
* ``create_task`` (background tasks, cancellation) – plus ``TaskGroup``,
  ``as_completed`` and ``timeout``
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import time
from collections.abc import Awaitable
from dataclasses import dataclass

DELIVERABLES: dict[str, str] = {
    "coroutine function (async def)": "fetch_status",
    "await": "fetch_status",
    "event loop (asyncio.run / get_running_loop)": "loop_facts",
    "gather": "board_with_gather",
    "gather with return_exceptions": "board_tolerant",
    "create_task and cancellation": "refresh_in_background",
    "TaskGroup (structured concurrency)": "board_with_taskgroup",
    "as_completed": "first_arrivals",
    "timeouts": "status_with_timeout",
}

LATENCY = {"LH": 0.05, "AI": 0.08, "BA": 0.03, "EK": 0.06}
STATUS = {"LH": "on time", "AI": "delayed 20m", "BA": "boarding", "EK": "on time"}


class AirlineUnavailable(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Flight:
    code: str
    status: str


async def fetch_status(airline: str, scale: float = 1.0) -> Flight:
    """A coroutine: calling it returns a coroutine object; ``await`` runs it."""
    if airline not in LATENCY:
        raise AirlineUnavailable(f"{airline} service is down")
    await asyncio.sleep(LATENCY[airline] * scale)  # yields control to the event loop
    return Flight(f"{airline}{100 + len(airline)}", STATUS[airline])


async def board_sequential(airlines: list[str]) -> list[Flight]:
    return [await fetch_status(a) for a in airlines]  # each waits for the previous one


async def board_with_gather(airlines: list[str]) -> list[Flight]:
    """All requests in flight at once; results keep the input order."""
    return list(await asyncio.gather(*(fetch_status(a) for a in airlines)))


async def board_tolerant(airlines: list[str]) -> dict[str, str]:
    """``return_exceptions=True`` turns failures into values instead of cancelling everything."""
    results = await asyncio.gather(*(fetch_status(a) for a in airlines), return_exceptions=True)
    return {a: (r.status if isinstance(r, Flight) else f"error: {r}") for a, r in zip(airlines, results, strict=True)}


async def board_with_taskgroup(airlines: list[str]) -> list[Flight]:
    """``TaskGroup`` cancels the remaining tasks if one fails and raises an ExceptionGroup."""
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch_status(a)) for a in airlines]
    return [t.result() for t in tasks]


async def first_arrivals(airlines: list[str]) -> list[str]:
    """Process results in completion order, fastest service first."""
    order = []
    for next_done in asyncio.as_completed([fetch_status(a) for a in airlines]):
        flight = await next_done
        order.append(flight.code[:2])
    return order


async def status_with_timeout(airline: str, seconds: float) -> str:
    try:
        async with asyncio.timeout(seconds):
            return (await fetch_status(airline)).status
    except TimeoutError:
        return "unknown (timed out)"


async def refresh_in_background(ticks: int, interval: float = 0.01) -> tuple[int, bool]:
    """``create_task`` starts work immediately; we can keep working and cancel it later."""
    refreshes = 0

    async def refresher() -> None:
        nonlocal refreshes
        while True:
            await asyncio.sleep(interval)
            refreshes += 1

    task = asyncio.create_task(refresher(), name="board-refresher")
    await asyncio.sleep(interval * ticks + interval / 2)
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task  # wait until the cancellation has actually been processed
    return refreshes, task.cancelled()


async def loop_facts() -> dict[str, object]:
    """The event loop is the scheduler that runs coroutines and callbacks."""
    loop = asyncio.get_running_loop()
    fired: list[str] = []
    loop.call_soon(fired.append, "call_soon")
    loop.call_later(0.01, fired.append, "call_later")
    await asyncio.sleep(0.02)
    return {"running": loop.is_running(), "callbacks": fired, "coroutine_is_lazy": _coroutine_is_lazy()}


def _coroutine_is_lazy() -> bool:
    """Calling a coroutine function runs *nothing* – the body waits for an await."""
    coro = fetch_status("LH")
    state = inspect.getcoroutinestate(coro)
    coro.close()  # never awaited – close it to avoid a "never awaited" warning
    return state == inspect.CORO_CREATED


async def timed[T](awaitable: Awaitable[T]) -> tuple[T, float]:
    start = time.perf_counter()
    result = await awaitable
    return result, round(time.perf_counter() - start, 3)


def main() -> None:
    airlines = list(LATENCY)
    print("Day 75 – Departures board\n")
    _, seq = asyncio.run(timed(board_sequential(airlines)))
    flights, conc = asyncio.run(timed(board_with_gather(airlines)))
    print(f"sequential {seq}s vs gather {conc}s →", [f"{f.code}: {f.status}" for f in flights])
    print("tolerant:", asyncio.run(board_tolerant(["LH", "XX", "BA"])))
    print("arrival order:", asyncio.run(first_arrivals(airlines)))
    print("timeout:", asyncio.run(status_with_timeout("AI", 0.01)))
    print("background refreshes, cancelled:", asyncio.run(refresh_in_background(3)))
    print("loop:", asyncio.run(loop_facts()))


if __name__ == "__main__":
    main()
