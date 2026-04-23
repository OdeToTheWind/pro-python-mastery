# src/day_37_python_turtle/main.py
"""
Day 37: Python Turtle – Interactive Graphics Explorer
With graceful fallback if Tkinter is not available.
"""

import sys

def main():
    print("Welcome to Day 37 – Python Turtle Graphics")
    print("Let's draw shapes using Python's Turtle module.\n")

    try:
        import turtle
        print("✅ Turtle module loaded successfully!\n")
        
        # Create screen and turtle
        screen = turtle.Screen()
        screen.title("Python Turtle Explorer - Day 37")
        screen.bgcolor("lightblue")

        t = turtle.Turtle()
        t.speed(6)
        t.pensize(3)
        t.pencolor("darkblue")

        while True:
            print("\n" + "─" * 50)
            print("Choose shape to draw:")
            print("  1) Square")
            print("  2) Circle")
            print("  3) Star")
            print("  4) Spiral")
            print("  5) Clear Screen")
            print("  6) Exit Turtle")
            print("─" * 50)

            choice = input("→ ").strip()

            if choice == "6":
                print("Closing Turtle Graphics...")
                break
            elif choice == "1":
                size = int(input("Square side length (default 100): ") or 100)
                for _ in range(4):
                    t.forward(size)
                    t.right(90)
            elif choice == "2":
                radius = int(input("Circle radius (default 80): ") or 80)
                t.circle(radius)
            elif choice == "3":
                size = int(input("Star size (default 100): ") or 100)
                for _ in range(5):
                    t.forward(size)
                    t.right(144)
            elif choice == "4":
                print("Drawing spiral...")
                for i in range(36):
                    t.forward(i * 6)
                    t.right(25)
            elif choice == "5":
                t.clear()
                print("Screen cleared.")
            else:
                print("Invalid choice. Please select 1-6.")

        screen.bye()

    except (ImportError, ModuleNotFoundError):
        print("❌ Turtle graphics not available (Tkinter/_tkinter missing)")
        print("This is common in some servers, WSL, or minimal Python installs.")
        print("To enable Turtle:")
        print("   sudo apt install python3-tk    # On Ubuntu/Debian")
        print("   or install full Python with Tk support")
        
    except Exception as e:
        print(f"❌ Turtle error: {e}")

    print("\nTurtle Graphics session ended.")
    print("You learned how to use Python's built-in graphics module!")
    print("Next: Game Development with Python and OOP (Day 38)\n")


if __name__ == "__main__":
    main()