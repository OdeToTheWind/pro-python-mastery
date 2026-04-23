# src/day_34_optional_required_default_parameters/main.py
"""
Day 34: Optional, Required and Default Parameters – Interactive Explorer
"""

def create_user(name: str, age: int, email: str = None, is_active: bool = True, role: str = "user"):
    """Demonstrates required, optional, and default parameters."""
    user = {
        "name": name,
        "age": age,
        "email": email or "not provided",
        "is_active": is_active,
        "role": role
    }
    return user


def calculate_price(base_price: float, quantity: int = 1, discount: float = 0.0, tax: float = 0.18):
    """Mix of required and optional parameters."""
    subtotal = base_price * quantity
    discount_amount = subtotal * discount
    tax_amount = (subtotal - discount_amount) * tax
    final_price = subtotal - discount_amount + tax_amount
    return round(final_price, 2)


def main():
    print("Welcome to Day 34 – Optional, Required and Default Parameters\n")

    print("Example 1: User Creation")
    name = input("Enter name: ").strip()
    age = int(input("Enter age: "))
    email = input("Enter email (press Enter to skip): ").strip() or None
    user = create_user(name, age, email)
    print("Created user:", user)

    print("\nExample 2: Price Calculator")
    price = float(input("Base price: "))
    qty = int(input("Quantity (default 1): ") or 1)
    disc = float(input("Discount % (default 0): ") or 0) / 100
    final = calculate_price(price, qty, disc)
    print(f"Final price after tax and discount: ₹{final}")

    print("\nYou now understand how to design flexible function signatures!")
    print("Next: Event Listeners (Day 35)\n")


if __name__ == "__main__":
    main()