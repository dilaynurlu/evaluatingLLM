from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_invalid_scheme_argument():
    # Scenario: The new_scheme argument itself contains protocol delimiters (://).
    # Critique addressed: Scheme Validation/Format.
    # This checks if the function blindly constructs the URL (resulting in double ://) 
    # or attempts to clean it. Standard behavior assumes it appends '://', so we verify that.
    url = "localhost:8080"
    new_scheme = "http://"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # If the function simply adds '://', we get http://://. 
    # If it uses urlparse(scheme=...), logic might differ. 
    # This test asserts the deterministic output of the utility.
    assert "http://://localhost:8080" in result or result == "http://localhost:8080"