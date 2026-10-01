"""Number formatting helpers."""


def percent(part: float, whole: float, digits: int = 1) -> str:
    if whole == 0:
        return "n/a"
    return f"{part / whole:.{digits}%}"
