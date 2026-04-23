# src/day_33_module_aliasing/main.py
"""
Day 33: Module Aliasing – Interactive Explorer
"""

import random as rnd
import datetime as dt
import math as m

def main():
    print("Welcome to Day 33 – Module Aliasing\n")

    print("Using alias 'rnd' for random module:")
    print(f"Random number between 1-100: {rnd.randint(1, 100)}")

    print("\nUsing alias 'dt' for datetime:")
    now = dt.datetime.now()
    print(f"Current time: {now.strftime('%H:%M:%S')}")

    print("\nUsing alias 'm' for math:")
    print(f"Pi ≈ {m.pi:.6f}")
    print(f"Square root of 144 = {m.sqrt(144)}")

    print("\nAliasing helps avoid name conflicts and shortens long module names.")
    print("Common pattern: import pandas as pd, import numpy as np")
    print("\nNext: Optional, Required and Default Parameters (Day 34)\n")


if __name__ == "__main__":
    main()