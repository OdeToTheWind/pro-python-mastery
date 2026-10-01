"""Tests for Day 57 – REST APIs & JSON."""

from datetime import UTC, datetime
from http import HTTPMethod, HTTPStatus

import pytest

from src.day_57_rest_apis_json.main import (
    METHOD_PROPERTIES,
    Request,
    Response,
    TodoAPI,
    dumps,
    main,
)


@pytest.fixture
def api():
    return TodoAPI()


def send(api, method, path, body=""):
    return api.handle(Request(method, path, body))


def test_method_properties():
    assert METHOD_PROPERTIES[HTTPMethod.GET] == {"safe": True, "idempotent": True}
    assert METHOD_PROPERTIES[HTTPMethod.PUT]["idempotent"] and not METHOD_PROPERTIES[HTTPMethod.POST]["idempotent"]


def test_dumps_encodes_datetime_and_rejects_unknown_types():
    assert dumps({"at": datetime(2026, 1, 1, tzinfo=UTC)}) == '{"at":"2026-01-01T00:00:00+00:00"}'
    with pytest.raises(TypeError):
        dumps({"x": object()})


def test_response_json_handles_scalars():
    assert Response(HTTPStatus.OK, "42").json() == 42
    assert Response(HTTPStatus.OK, "null").json() is None
    assert Response(HTTPStatus.NO_CONTENT).json() is None
    assert not Response(HTTPStatus.NOT_FOUND).ok


def test_create_and_read(api):
    created = send(api, HTTPMethod.POST, "/todos", '{"title": "  Write tests "}')
    assert created.status == HTTPStatus.CREATED
    assert created.json()["title"] == "Write tests" and created.json()["id"] == 1
    assert send(api, HTTPMethod.GET, "/todos/1").json()["done"] is False
    assert len(send(api, HTTPMethod.GET, "/todos").json()) == 1


@pytest.mark.parametrize(
    ("body", "status"),
    [("{bad", HTTPStatus.BAD_REQUEST), ("[1]", HTTPStatus.UNPROCESSABLE_ENTITY),
     ('{"done": true}', HTTPStatus.UNPROCESSABLE_ENTITY), ('{"title": ""}', HTTPStatus.UNPROCESSABLE_ENTITY),
     ('{"title": "x", "owner": "me"}', HTTPStatus.UNPROCESSABLE_ENTITY),
     ('{"title": "x", "done": "yes"}', HTTPStatus.UNPROCESSABLE_ENTITY)],
)
def test_post_validation(api, body, status):
    response = send(api, HTTPMethod.POST, "/todos", body)
    assert response.status == status
    assert response.json()["error"] == status.phrase


def test_content_type_is_checked(api):
    request = Request(HTTPMethod.POST, "/todos", "title=x", {"Content-Type": "application/x-www-form-urlencoded"})
    assert api.handle(request).status == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_patch_is_partial(api):
    send(api, HTTPMethod.POST, "/todos", '{"title": "a"}')
    patched = send(api, HTTPMethod.PATCH, "/todos/1", '{"done": true}').json()
    assert patched["title"] == "a" and patched["done"] is True


def test_put_creates_then_replaces_idempotently(api):
    first = send(api, HTTPMethod.PUT, "/todos/7", '{"title": "x"}')
    second = send(api, HTTPMethod.PUT, "/todos/7", '{"title": "x"}')
    assert (first.status, second.status) == (HTTPStatus.CREATED, HTTPStatus.OK)
    assert len(api.todos) == 1
    assert send(api, HTTPMethod.POST, "/todos", '{"title": "next"}').json()["id"] == 8


def test_delete_then_not_found(api):
    send(api, HTTPMethod.POST, "/todos", '{"title": "a"}')
    deleted = send(api, HTTPMethod.DELETE, "/todos/1")
    assert deleted.status == HTTPStatus.NO_CONTENT and deleted.body == ""
    assert send(api, HTTPMethod.DELETE, "/todos/1").status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ("method", "path", "status"),
    [(HTTPMethod.GET, "/users", HTTPStatus.NOT_FOUND), (HTTPMethod.GET, "/todos/abc", HTTPStatus.BAD_REQUEST),
     (HTTPMethod.DELETE, "/todos", HTTPStatus.METHOD_NOT_ALLOWED), (HTTPMethod.GET, "/todos/1/x", HTTPStatus.NOT_FOUND)],
)
def test_routing_errors(api, method, path, status):
    assert send(api, method, path).status == status


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "201 Created" in out and "204 No Content" in out and "422 Unprocessable" in out
