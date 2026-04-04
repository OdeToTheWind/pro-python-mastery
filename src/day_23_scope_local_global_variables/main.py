# src/day_23_scope_local_global_variables/main.py
"""
Day 23: Scope and Local/Global Variables – Interactive Explorer
Master LEGB rule, global, nonlocal, and why global variables are often dangerous.
"""

# Global variable for demonstration (defined at module level)
global_counter = 0


def print_scope_guide():
    print("\n" + "═" * 70)
    print("Scope & LEGB Rule – Quick Reference (Day 23)")
    print("═" * 70)
    print("LEGB Rule (order Python looks for variables):")
    print("  L - Local (inside current function)")
    print("  E - Enclosing (nested functions)")
    print("  G - Global (module level)")
    print("  B - Built-in (len, sum, print, etc.)")
    print("")
    print("global keyword → modifies global variable from inside function")
    print("nonlocal keyword → modifies variable from enclosing scope")
    print("Best practice: Avoid global variables when possible")
    print("═" * 70)


def main():
    print("Welcome to Day 23 – Scope and Local/Global Variables!")
    print("Understanding scope is crucial for writing bug-free code.\n")

    print_scope_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Scope Demo:")
        print("  1) Local vs Global Variables")
        print("  2) Modifying Global with 'global' keyword")
        print("  3) Nested Functions and 'nonlocal'")
        print("  4) LEGB Rule Demonstration")
        print("  5) Why Global Variables Are Dangerous")
        print("  6) Practical Example: Counter with Scope")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nLocal vs Global")
                x = 10  # local variable
                
                def inner_function():
                    x = 20  # creates a new local variable
                    print(f"Inside function (local x): {x}")
                
                inner_function()
                print(f"Outside function (global x): {x}")

            elif choice == "2":
                print("\nModifying Global Variable")
                print(f"Global counter before: {global_counter}")
                
                def increment_counter():
                    global global_counter   # declare global at the top of the function
                    global_counter += 1
                    print(f"Inside function - counter increased to {global_counter}")
                
                increment_counter()
                print(f"Global counter after: {global_counter}")

            elif choice == "3":
                print("\nNested Functions and 'nonlocal'")
                def outer():
                    count = 0
                    
                    def inner():
                        nonlocal count   # refers to enclosing scope
                        count += 1
                        print(f"Inner function - count is now {count}")
                    
                    inner()
                    inner()
                    print(f"Outer function - final count: {count}")
                
                outer()

            elif choice == "4":
                print("\nLEGB Rule Demonstration")
                x = "global"
                
                def outer_func():
                    x = "enclosing"
                    
                    def inner_func():
                        x = "local"
                        print(f"Inside inner_func: {x}")
                    
                    inner_func()
                    print(f"Inside outer_func: {x}")
                
                outer_func()
                print(f"Global scope: {x}")

            elif choice == "5":
                print("\nWhy Global Variables Are Dangerous")
                print("Problem: Any function can modify them → hard to debug")
                print("Better approach: Pass values as parameters and return results")
                
                def bad_example():
                    global global_counter
                    global_counter += 100   # unexpected side effect
                
                def good_example(current_count):
                    return current_count + 100
                
                print("Bad way (using global):")
                bad_example()
                print(f"Global counter changed unexpectedly: {global_counter}")
                
                print("\nGood way (return value):")
                new_value = good_example(50)
                print(f"New value returned: {new_value}")

            elif choice == "6":
                print("\nPractical Counter Example")
                count = 0
                
                def increment():
                    nonlocal count
                    count += 1
                    return count
                
                for _ in range(5):
                    print(f"Count after increment: {increment()}")
                
                print(f"Final count outside: {count}")

            else:
                print("Please choose 1-6.")

        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nExcellent! You now understand variable scope in Python.")
    print("Remember the LEGB rule and prefer passing parameters over using globals.")
    print("Next: Debugging Techniques (Day 24) - last day of Beginner Projects!\n")


if __name__ == "__main__":
    main()