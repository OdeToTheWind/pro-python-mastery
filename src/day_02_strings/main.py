"""
Day 2: String Manipulation - Professional Profile Generator
Focus: F-strings, slicing, strip/replace, and case methods.
"""

def generate_profile(raw_name: str, role: str, experience_years: int) -> str:
    # 1. Data Cleaning: Strip whitespace and capitalize properly
    clean_name = raw_name.strip().title()
    
    # 2. String Transformation: Create a unique ID from the name (slicing + case)
    # Take first 3 letters of name + experience count
    user_handle = f"@{clean_name[:3].lower()}{experience_years:02}"
    
    # 3. Professional Formatting: Using f-string alignment and padding
    # <20 means left-align with a width of 20 characters
    header = f"{'PROFILE REPORT':^30}" # Center aligned
    divider = "-" * 30
    
    profile_output = (
        f"{header}\n"
        f"{divider}\n"
        f"Name:       {clean_name:<20}\n"
        f"Handle:     {user_handle:<20}\n"
        f"Role:       {role.upper():<20}\n"
        f"Exp:        {experience_years} Years\n"
        f"{divider}"
    )
    
    return profile_output

def run_string_demonstration():
    # Input simulating slightly messy data
    raw_user_input = "  johN dOe  "
    current_role = "Senior Software Engineer"
    years = 8

    report = generate_profile(raw_user_input, current_role, years)
    print(report)

if __name__ == "__main__":
    run_string_demonstration()