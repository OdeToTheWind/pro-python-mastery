"""Tests for Day 78 – Testing with pytest.

This file *is* the lesson. Read it top to bottom:

1. fixtures: plain, factory, yield (teardown), scoped, and built-ins
   (tmp_path, monkeypatch, capsys)
2. parametrisation: tables, ids, stacked decorators, ``pytest.param`` with marks
3. mocking: ``Mock(spec=...)``, ``side_effect``, ``patch.object``, call assertions
4. coverage: ``measure_coverage`` and ``pytest --cov``
"""

from decimal import ROUND_HALF_UP, Decimal
from unittest.mock import Mock, patch

import pytest

from src.day_78_testing_with_pytest import main as day78
from src.day_78_testing_with_pytest.main import (
    ZONE_CASES,
    CarrierError,
    FakeCarrier,
    QuoteService,
    make_parcel,
    measure_coverage,
    zone,
)

# --------------------------------------------------------------------------- fixtures


@pytest.fixture
def carrier():
    """A fresh fake for each test – tests never share state."""
    return FakeCarrier()


@pytest.fixture
def service(carrier):
    """Fixtures can depend on other fixtures."""
    return QuoteService(carrier, clock=lambda: 1000.0)


@pytest.fixture
def parcel_factory():
    """A *factory* fixture: tests build exactly the parcel they need."""
    created = []

    def build(**overrides):
        parcel = make_parcel(**overrides)
        created.append(parcel)
        return parcel

    yield build
    # code after `yield` is teardown – runs even if the test fails
    created.clear()


@pytest.fixture(scope="module")
def rate_table():
    """Module scope: built once and shared by every test in this file (keep it read-only)."""
    return {code: zone("DE", code) for code in ("DE", "FR", "US")}


def test_fixture_composition(service, carrier, parcel_factory):
    assert service.quote(parcel_factory()) == Decimal("6.39")  # 3.99 + 1.20 × 2 kg
    assert carrier.calls == [("DE", "DE", 2.0)]


def test_module_scoped_fixture(rate_table):
    assert rate_table == {"DE": "domestic", "FR": "eu", "US": "world"}


# ----------------------------------------------------------------- parametrisation


@pytest.mark.parametrize(("origin", "destination", "expected"), ZONE_CASES,
                         ids=[f"{o}-{d}" for o, d, _ in ZONE_CASES])
def test_zone(origin, destination, expected):
    assert zone(origin, destination) == expected


@pytest.mark.parametrize("express", [False, True], ids=["standard", "express"])
@pytest.mark.parametrize("destination", ["DE", "FR", "US"])
def test_price_matrix(service, parcel_factory, express, destination):
    """Stacked parametrize → 2 × 3 = 6 test cases."""
    carrier_base = Decimal("3.99") + Decimal("1.20") * 2  # what FakeCarrier charges for 2 kg
    expected = carrier_base + {"DE": Decimal("0"), "FR": Decimal("4.50"), "US": Decimal("19.00")}[destination]
    if express:
        expected *= Decimal("1.5")
    price = service.quote(parcel_factory(destination=destination, express=express))
    # Beware: `assert a == b if cond else c` parses as `assert (a == b) if cond else c`.
    assert price == expected.quantize(Decimal("0.01"), ROUND_HALF_UP)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        pytest.param({"weight_kg": 0}, "positive", id="zero-weight"),
        pytest.param({"weight_kg": 40}, "exceeds", id="too-heavy"),
        pytest.param({"length_cm": 120, "width_cm": 80, "height_cm": 40}, "exceeds", id="too-bulky"),
    ],
)
def test_invalid_parcels(service, parcel_factory, overrides, message):
    with pytest.raises(ValueError, match=message):
        service.quote(parcel_factory(**overrides))


@pytest.mark.parametrize(("dims", "chargeable"), [((10, 10, 10), 2.0), ((50, 40, 30), 12.0)])
def test_volumetric_weight(parcel_factory, dims, chargeable):
    length, width, height = dims
    assert parcel_factory(length_cm=length, width_cm=width, height_cm=height).chargeable_kg == chargeable


# ------------------------------------------------------------------------- mocking


def test_mock_with_spec_and_call_assertions(parcel_factory):
    api = Mock(spec=FakeCarrier)  # spec: calling a method the real class lacks is an error
    api.base_rate.return_value = Decimal("10.00")
    service = QuoteService(api, clock=lambda: 0.0)
    assert service.quote(parcel_factory(destination="US")) == Decimal("29.00")
    api.base_rate.assert_called_once_with("DE", "US", 2.0)
    with pytest.raises(AttributeError):
        api.delete_everything()


def test_side_effect_turns_timeouts_into_domain_errors(parcel_factory):
    api = Mock(spec=FakeCarrier)
    api.base_rate.side_effect = TimeoutError
    with pytest.raises(CarrierError) as info:
        QuoteService(api).quote(parcel_factory())
    assert isinstance(info.value.__cause__, TimeoutError)


def test_cache_respects_ttl_with_controllable_clock(carrier, parcel_factory):
    now = [0.0]
    service = QuoteService(carrier, clock=lambda: now[0])
    service.quote(parcel_factory())
    now[0] = 59
    service.quote(parcel_factory())
    assert len(carrier.calls) == 1  # served from cache
    now[0] = 61
    service.quote(parcel_factory())
    assert len(carrier.calls) == 2  # expired → carrier called again


def test_patch_object_spies_on_a_real_method(service, parcel_factory, carrier):
    with patch.object(carrier, "base_rate", wraps=carrier.base_rate) as spy:
        service.quote(parcel_factory(weight_kg=5))
    spy.assert_called_once()
    assert spy.call_args.args == ("DE", "DE", 5.0)


def test_monkeypatch_module_attribute(monkeypatch, parcel_factory, service):
    monkeypatch.setitem(day78.ZONE_SURCHARGE, "domestic", Decimal("1.00"))
    assert service.quote(parcel_factory()) == Decimal("7.39")  # undone automatically after the test


# ------------------------------------------------------------- built-ins & coverage


def test_tmp_path_and_capsys(tmp_path, capsys, service, parcel_factory):
    report = tmp_path / "quote.txt"
    report.write_text(str(service.quote(parcel_factory())), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))
    assert capsys.readouterr().out == "6.39\n"


def test_measure_coverage_reports_partial_execution():
    result = measure_coverage(lambda: QuoteService(FakeCarrier()).quote(make_parcel()))
    assert 0 < result["percent"] < 100
    assert result["missing"] > 0 and result["statements"] > result["missing"]


def test_main_runs(capsys):
    from src.day_78_testing_with_pytest.main import main

    main()
    assert "DE→US (world   ) €25.39" in capsys.readouterr().out
