# Pro-tip: Use type hints (e.g., : str) to show you understand modern Python
def variable_demonstration():
    project_name: str = "Pro Python Mastery"
    days_completed: int = 1
    is_active: bool = True

    # Use F-strings for professional formatting
    print(f"Project: {project_name}")
    print(f"Status: Day {days_completed} - Challenge Active: {is_active}")

if __name__ == "__main__":
    variable_demonstration()