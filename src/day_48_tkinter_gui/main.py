"""Day 48 – Creating Desktop GUI Apps with Tkinter.

Scenario: a *restaurant tip splitter* desktop app. The calculation is a pure
function (unit-tested everywhere); the GUI is a thin layer of widgets laid
out with ``grid`` that reads user input and shows results or errors.

Deliverables (syllabus):
* GUI building with widgets (Label, Entry, Spinbox, Scale, Button, Checkbutton)
* Layouts (``grid`` with rows, columns, ``sticky`` and padding)
* User input (reading, validating and reacting to Entry values / events)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

DELIVERABLES: dict[str, str] = {
    "widgets": "TipApp.build",
    "grid layout": "TipApp.build",
    "user input handling": "TipApp.calculate",
    "input validation (pure, testable)": "calculate_tip",
    "event binding": "TipApp.build",
}


@dataclass(frozen=True, slots=True)
class TipResult:
    tip: Decimal
    total: Decimal
    per_person: Decimal


def calculate_tip(bill_text: str, percent: int, people_text: str, round_up: bool = False) -> TipResult:
    """Validate raw widget text and compute the split. Raises ``ValueError`` with a friendly message."""
    try:
        bill = Decimal(bill_text.strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError("Bill must be a number, e.g. 48.50") from None
    if bill <= 0:
        raise ValueError("Bill must be greater than zero")
    if not 0 <= percent <= 30:
        raise ValueError("Tip must be between 0 % and 30 %")
    if not people_text.strip().isdigit() or int(people_text) < 1:
        raise ValueError("People must be a whole number ≥ 1")
    people = int(people_text)
    cent = Decimal("0.01")
    tip = (bill * percent / 100).quantize(cent, ROUND_HALF_UP)
    total = bill + tip
    per_person = (total / people).quantize(cent, ROUND_HALF_UP)
    if round_up:
        per_person = per_person.to_integral_value(rounding="ROUND_CEILING")
        total = per_person * people
        tip = total - bill
    return TipResult(tip, total, per_person)


class TipApp:  # pragma: no cover – exercised only where a display exists
    def __init__(self, root: Any) -> None:
        import tkinter as tk

        self.tk = tk
        self.root = root
        self.bill = tk.StringVar(value="")
        self.people = tk.StringVar(value="2")
        self.percent = tk.IntVar(value=12)
        self.round_up = tk.BooleanVar(value=False)
        self.output = tk.StringVar(value="Enter the bill and press Calculate")
        self.build()

    def build(self) -> None:
        tk = self.tk
        self.root.title("Tip Splitter – Day 48")
        frame = tk.Frame(self.root, padx=16, pady=16)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Bill (€)").grid(row=0, column=0, sticky="w", pady=4)
        bill_entry = tk.Entry(frame, textvariable=self.bill, width=12)
        bill_entry.grid(row=0, column=1, sticky="ew")
        bill_entry.focus_set()

        tk.Label(frame, text="Tip %").grid(row=1, column=0, sticky="w", pady=4)
        tk.Scale(frame, from_=0, to=30, orient="horizontal", variable=self.percent).grid(
            row=1, column=1, sticky="ew")

        tk.Label(frame, text="People").grid(row=2, column=0, sticky="w", pady=4)
        tk.Spinbox(frame, from_=1, to=20, textvariable=self.people, width=5).grid(row=2, column=1, sticky="w")

        tk.Checkbutton(frame, text="Round each share up", variable=self.round_up).grid(
            row=3, column=0, columnspan=2, sticky="w")
        tk.Button(frame, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=2, pady=8)
        self.result_label = tk.Label(frame, textvariable=self.output, font=("Helvetica", 12))
        self.result_label.grid(row=5, column=0, columnspan=2)
        self.root.bind("<Return>", lambda _event: self.calculate())

    def calculate(self) -> None:
        try:
            result = calculate_tip(self.bill.get(), self.percent.get(), self.people.get(), self.round_up.get())
        except ValueError as exc:
            self.output.set(f"⚠ {exc}")
            self.result_label.configure(fg="red")
            return
        self.output.set(f"Tip €{result.tip}  ·  Total €{result.total}  ·  Each €{result.per_person}")
        self.result_label.configure(fg="black")


def main() -> None:  # pragma: no cover – opens a window
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter is not installed (Linux: sudo apt install python3-tk).")
        print("Text demo instead:", calculate_tip("86.40", 15, "3"))
        return
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print(f"No display available ({exc}). Text demo instead:", calculate_tip("86.40", 15, "3"))
        return
    TipApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
