"""Tests for Day 45 – List Comprehensions."""

from src.day_45_list_comprehensions.main import (
    LOG,
    flatten,
    loop_equivalent,
    main,
    memory_comparison,
    normalise_paths,
    parse,
    server_errors,
    slow_requests,
    status_codes,
    status_labels,
    transpose,
)


def test_parse_skips_malformed_lines():
    assert len(parse(LOG)) == 5


def test_status_codes():
    assert status_codes(LOG) == [200, 500, 401, 304, 503]


def test_filtering():
    assert server_errors(LOG) == ["/api/users?id=7", "/api/orders"]
    assert server_errors(["bad"]) == []


def test_comprehension_matches_loop():
    assert server_errors(LOG) == loop_equivalent(LOG)


def test_transformation():
    assert normalise_paths(LOG) == ["/index.html", "/api/users", "/api/login", "/images/logo.png", "/api/orders"]


def test_status_labels_conditional_expression():
    assert status_labels([200, 301, 404, 503]) == ["ok", "redirect", "client", "server"]


def test_walrus_filter():
    assert slow_requests(LOG, 1.0) == [("/api/users?id=7", 1.54), ("/api/orders", 2.9)]
    assert slow_requests(LOG, 10) == []


def test_nested_comprehensions():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([]) == []
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]


def test_generator_uses_less_memory():
    list_bytes, gen_bytes = memory_comparison(10_000)
    assert gen_bytes < list_bytes / 100


def test_main(capsys):
    main()
    assert "labels      : ['ok', 'server', 'client', 'redirect', 'server']" in capsys.readouterr().out
