# src/day_47_packing_unpacking/main.py
"""
Day 47: Packing and Unpacking Functions – Interactive Explorer
"""

def main():
    print("Welcome to Day 47 – Packing and Unpacking\n")

    # Unpacking
    print("Unpacking examples:")
    coords = (10, 20, 30)
    x, y, z = coords
    print(f"Unpacked tuple: x={x}, y={y}, z={z}")

    # Packing with *args
    def sum_all(*args):
        return sum(args)

    print(f"Sum of 1,2,3,4,5 = {sum_all(1,2,3,4,5)}")

    # Unpacking with **
    def print_info(**kwargs):
        for key, value in kwargs.items():
            print(f"{key}: {value}")

    print_info(name="Alice", age=25, city="Bengaluru")

    print("\n*args and **kwargs allow flexible function calls.")
    print("Next: Creating Desktop GUI Apps with Tkinter (Day 48)\n")


if __name__ == "__main__":
    main()