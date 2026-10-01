"""Tests for Day 39 – Inheritance."""

import pytest

from src.day_39_python_inheritance.main import (
    BatteryMixin,
    Camera,
    Device,
    SmartDoorbell,
    WiFiMixin,
    capabilities,
    main,
    mro_names,
)


def test_single_inheritance_reuses_and_extends():
    cam = Camera("cam", "4K")
    assert isinstance(cam, Device) and issubclass(Camera, Device)
    assert cam.power_on() == "cam on"  # inherited
    assert cam.status() == "cam: on [4K, idle]"  # overridden + extended via super()


def test_camera_requires_power():
    with pytest.raises(RuntimeError):
        Camera("cam").record()


def test_multiple_inheritance_initialises_every_parent():
    bell = SmartDoorbell(name="door", ssid="villa", battery=55, resolution="2K")
    assert (bell.name, bell.ssid, bell.battery, bell.resolution) == ("door", "villa", 55, "2K")
    assert bell.powered is False and bell.connected is False


def test_mro_order():
    assert mro_names(SmartDoorbell) == [
        "SmartDoorbell", "WiFiMixin", "BatteryMixin", "Camera", "Device", "object",
    ]


def test_cooperative_status_chain_follows_mro():
    bell = SmartDoorbell(name="door", battery=80)
    bell.power_on()
    bell.connect()
    assert bell.status() == "door: on [1080p, idle] battery=80% wifi=up"
    assert bell.ring() == "door rang – recording"


def test_mixin_validation_still_runs():
    with pytest.raises(ValueError):
        SmartDoorbell(name="door", battery=120)


def test_capabilities_via_isinstance():
    assert capabilities(Device("d")) == []
    assert capabilities(Camera("c")) == ["video"]
    assert capabilities(SmartDoorbell(name="b")) == ["video", "wifi", "battery"]
    assert issubclass(SmartDoorbell, WiFiMixin) and issubclass(SmartDoorbell, BatteryMixin)


def test_main(capsys):
    main()
    assert "MRO: SmartDoorbell → WiFiMixin" in capsys.readouterr().out
