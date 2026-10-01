"""Day 39 – Python Inheritance.

Scenario: a *smart-device product line*. A base ``Device`` is specialised by
single inheritance (``Camera``) and combined with capability mixins through
multiple inheritance (``SmartDoorbell``) using cooperative ``super()``.

Deliverables (syllabus):
* Single inheritance
* Multiple inheritance (mixins, MRO, the diamond)
* ``super()`` (cooperative, with ``**kwargs`` forwarding)
* Method overriding (and extending the parent's version)
"""

from __future__ import annotations

from typing import Any

DELIVERABLES: dict[str, str] = {
    "single inheritance": "Camera",
    "multiple inheritance": "SmartDoorbell",
    "super() and cooperative __init__": "WiFiMixin.__init__",
    "method overriding": "Camera.status",
    "method resolution order (MRO)": "mro_names",
    "isinstance / issubclass checks": "capabilities",
}


class Device:
    def __init__(self, name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)  # keeps the chain going for any mixin after us
        self.name = name
        self.powered = False

    def power_on(self) -> str:
        self.powered = True
        return f"{self.name} on"

    def status(self) -> str:
        return f"{self.name}: {'on' if self.powered else 'off'}"


class Camera(Device):
    """Single inheritance: a Camera *is a* Device."""

    def __init__(self, name: str, resolution: str = "1080p", **kwargs: Any) -> None:
        super().__init__(name, **kwargs)
        self.resolution = resolution
        self.recording = False

    def record(self) -> str:
        if not self.powered:
            raise RuntimeError("power on first")
        self.recording = True
        return "recording"

    def status(self) -> str:  # override and *extend* the parent's result
        return f"{super().status()} [{self.resolution}, {'REC' if self.recording else 'idle'}]"


class WiFiMixin:
    """Adds networking to any class it is mixed into."""

    def __init__(self, ssid: str = "home", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.ssid = ssid
        self.connected = False

    def connect(self) -> str:
        self.connected = True
        return f"connected to {self.ssid}"

    def status(self) -> str:
        return f"{super().status()} wifi={'up' if self.connected else 'down'}"  # type: ignore[misc]


class BatteryMixin:
    def __init__(self, battery: int = 100, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not 0 <= battery <= 100:
            raise ValueError("battery must be 0–100")
        self.battery = battery

    def status(self) -> str:
        return f"{super().status()} battery={self.battery}%"  # type: ignore[misc]


class SmartDoorbell(WiFiMixin, BatteryMixin, Camera):
    """Multiple inheritance: mixins first, the concrete base class last."""

    def ring(self) -> str:
        return f"{self.name} rang – {self.record()}"


def mro_names(cls: type) -> list[str]:
    return [klass.__name__ for klass in cls.__mro__]


def capabilities(device: object) -> list[str]:
    caps = []
    if isinstance(device, Camera):
        caps.append("video")
    if isinstance(device, WiFiMixin):
        caps.append("wifi")
    if isinstance(device, BatteryMixin):
        caps.append("battery")
    return caps


def main() -> None:
    print("Day 39 – Smart device inheritance\n")
    cam = Camera("Garage cam", "4K")
    bell = SmartDoorbell(name="Front door", ssid="villa", battery=80, resolution="2K")
    cam.power_on()
    bell.power_on()
    bell.connect()
    print(bell.ring())
    print(cam.status())
    print(bell.status())
    print("MRO:", " → ".join(mro_names(SmartDoorbell)))
    print("Capabilities:", capabilities(cam), capabilities(bell))


if __name__ == "__main__":
    main()
