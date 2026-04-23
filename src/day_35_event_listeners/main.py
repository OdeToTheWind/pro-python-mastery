# src/day_35_event_listeners/main.py
"""
Day 35: Event Listeners – Interactive Explorer
Simulating event-driven programming with callback functions.
"""

def on_button_click(callback):
    print("Button clicked!")
    callback()

def on_key_press(key, callback):
    print(f"Key pressed: {key}")
    callback(key)

def main():
    print("Welcome to Day 35 – Event Listeners\n")

    def greet():
        print("Hello from event handler!")

    def log_key(key):
        print(f"Logged key press: {key.upper()}")

    print("Simulating button click event...")
    on_button_click(greet)

    print("\nSimulating key press event...")
    on_key_press("Enter", log_key)

    print("\nEvent listeners allow decoupling of event occurrence from event handling.")
    print("This pattern is widely used in GUI, web, and game development.")
    print("\nNext topics coming soon.\n")


if __name__ == "__main__":
    main()