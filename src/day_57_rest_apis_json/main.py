"""Day 57 – REST APIs & JSON.

Scenario: a *to-do list REST API* simulated in memory. No network: the goal is
to understand what HTTP methods mean, which status code each outcome deserves,
and how JSON request/response bodies are produced and consumed.

Deliverables (syllabus):
* HTTP methods (GET, POST, PUT, PATCH, DELETE – safe vs idempotent)
* Status codes (2xx/4xx/5xx and when to use each)
* Serialisation (Python ↔ JSON, explicit encoder, no lossy fallbacks)
* API payload processing (validation, error bodies, ``Content-Type``)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from http import HTTPMethod, HTTPStatus
from typing import Any

DELIVERABLES: dict[str, str] = {
    "HTTP methods and their semantics": "METHOD_PROPERTIES",
    "status codes": "TodoAPI.handle",
    "serialisation with an explicit encoder": "dumps",
    "deserialisation of request bodies": "Request.json",
    "payload validation and error bodies": "TodoAPI._validate",
    "response objects": "Response",
}

METHOD_PROPERTIES: dict[HTTPMethod, dict[str, bool]] = {
    HTTPMethod.GET: {"safe": True, "idempotent": True},
    HTTPMethod.POST: {"safe": False, "idempotent": False},
    HTTPMethod.PUT: {"safe": False, "idempotent": True},
    HTTPMethod.PATCH: {"safe": False, "idempotent": False},
    HTTPMethod.DELETE: {"safe": False, "idempotent": True},
}


def _encode(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"{type(value).__name__} is not JSON serialisable")  # fail loudly, never str()


def dumps(data: Any) -> str:
    return json.dumps(data, default=_encode, ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class Request:
    method: HTTPMethod
    path: str
    body: str = ""
    headers: dict[str, str] = field(default_factory=dict)

    def json(self) -> Any:
        if self.headers.get("Content-Type", "application/json").split(";")[0] != "application/json":
            raise ValueError("Content-Type must be application/json")
        return json.loads(self.body) if self.body else None


@dataclass(frozen=True, slots=True)
class Response:
    status: HTTPStatus
    body: str = ""
    headers: dict[str, str] = field(default_factory=lambda: {"Content-Type": "application/json"})

    @property
    def ok(self) -> bool:
        return self.status.is_success

    def json(self) -> Any:
        """Any JSON value is valid – including numbers, booleans and ``null``."""
        return json.loads(self.body) if self.body else None


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class TodoAPI:
    """A tiny REST resource at ``/todos`` and ``/todos/<id>``."""

    def __init__(self) -> None:
        self.todos: dict[int, Todo] = {}
        self._next_id = 1

    @staticmethod
    def _reply(status: HTTPStatus, payload: Any = None) -> Response:
        return Response(status, "" if payload is None else dumps(payload))

    @staticmethod
    def _error(status: HTTPStatus, message: str) -> Response:
        return TodoAPI._reply(status, {"error": status.phrase, "detail": message})

    @staticmethod
    def _validate(payload: Any, *, partial: bool) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("body must be a JSON object")
        unknown = set(payload) - {"title", "done"}
        if unknown:
            raise ValueError(f"unknown fields: {sorted(unknown)}")
        if not partial and "title" not in payload:
            raise ValueError("'title' is required")
        if "title" in payload and (not isinstance(payload["title"], str) or not payload["title"].strip()):
            raise ValueError("'title' must be a non-empty string")
        if "done" in payload and not isinstance(payload["done"], bool):
            raise ValueError("'done' must be true or false")
        return payload

    def handle(self, request: Request) -> Response:
        parts = [p for p in request.path.split("/") if p]
        if not parts or parts[0] != "todos" or len(parts) > 2:
            return self._error(HTTPStatus.NOT_FOUND, f"no route for {request.path}")
        try:
            if len(parts) == 1:
                return self._collection(request)
            if not parts[1].isdigit():
                return self._error(HTTPStatus.BAD_REQUEST, "id must be an integer")
            return self._item(request, int(parts[1]))
        except (ValueError, json.JSONDecodeError) as exc:
            status = HTTPStatus.UNPROCESSABLE_ENTITY if not isinstance(exc, json.JSONDecodeError) else HTTPStatus.BAD_REQUEST
            if "Content-Type" in str(exc):
                status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            return self._error(status, str(exc))

    def _collection(self, request: Request) -> Response:
        if request.method == HTTPMethod.GET:
            return self._reply(HTTPStatus.OK, [asdict(t) for t in self.todos.values()])
        if request.method == HTTPMethod.POST:
            data = self._validate(request.json(), partial=False)
            todo = Todo(self._next_id, data["title"].strip(), data.get("done", False))
            self.todos[todo.id] = todo
            self._next_id += 1
            return self._reply(HTTPStatus.CREATED, asdict(todo))
        return self._error(HTTPStatus.METHOD_NOT_ALLOWED, f"{request.method} not allowed on /todos")

    def _item(self, request: Request, todo_id: int) -> Response:
        todo = self.todos.get(todo_id)
        if request.method == HTTPMethod.PUT:  # full replacement – creates or overwrites
            data = self._validate(request.json(), partial=False)
            created = todo is None
            self.todos[todo_id] = Todo(todo_id, data["title"].strip(), data.get("done", False))
            self._next_id = max(self._next_id, todo_id + 1)
            return self._reply(HTTPStatus.CREATED if created else HTTPStatus.OK, asdict(self.todos[todo_id]))
        if todo is None:
            return self._error(HTTPStatus.NOT_FOUND, f"todo {todo_id} does not exist")
        if request.method == HTTPMethod.GET:
            return self._reply(HTTPStatus.OK, asdict(todo))
        if request.method == HTTPMethod.PATCH:
            data = self._validate(request.json(), partial=True)
            todo.title = data.get("title", todo.title).strip()
            todo.done = data.get("done", todo.done)
            return self._reply(HTTPStatus.OK, asdict(todo))
        if request.method == HTTPMethod.DELETE:
            del self.todos[todo_id]
            return self._reply(HTTPStatus.NO_CONTENT)
        return self._error(HTTPStatus.METHOD_NOT_ALLOWED, f"{request.method} not allowed")


def main() -> None:
    api = TodoAPI()
    calls = [
        Request(HTTPMethod.POST, "/todos", '{"title": "Learn REST"}'),
        Request(HTTPMethod.POST, "/todos", '{"done": "yes"}'),
        Request(HTTPMethod.PATCH, "/todos/1", '{"done": true}'),
        Request(HTTPMethod.GET, "/todos/1"),
        Request(HTTPMethod.PUT, "/todos/5", '{"title": "Created with PUT"}'),
        Request(HTTPMethod.DELETE, "/todos/1"),
        Request(HTTPMethod.DELETE, "/todos/1"),
        Request(HTTPMethod.POST, "/todos", "{not json"),
    ]
    print("Day 57 – In-memory REST API\n")
    for method, props in METHOD_PROPERTIES.items():
        print(f"  {method:<7} safe={props['safe']!s:<5} idempotent={props['idempotent']}")
    print()
    for request in calls:
        response = api.handle(request)
        print(f"{request.method:<6} {request.path:<9} → {response.status.value} {response.status.phrase:<22} {response.body[:60]}")


if __name__ == "__main__":
    main()
