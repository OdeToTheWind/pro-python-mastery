from src.day_02_strings.main import generate_profile

def test_profile_generation_logic():
    # Test name cleaning and handle generation
    result = generate_profile("  alice smith  ", "Developer", 5)
    
    assert "Alice Smith" in result
    assert "@ali05" in result
    assert "DEVELOPER" in result

def test_string_alignment():
    # Verify the output contains our expected fixed-width separators
    result = generate_profile("Bob", "Manager", 10)
    lines = result.split("\n")
    
    # Check if the header is centered (30 chars)
    assert len(lines[0]) == 30
    assert "PROFILE REPORT" in lines[0]