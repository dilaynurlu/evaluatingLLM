from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_dangerous_scheme_injection():
    # Scenario: Using a dangerous scheme (e.g., javascript) to verify input handling.
    # Critique addressed: Dangerous Schemes (XSS Vectors).
    # The function is expected to blindly prepend the provided scheme, verifying that
    # no unexpected sanitization or errors occur, allowing downstream components to handle validation.
    url = "//example.com/xss"
    new_scheme = "javascript"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "javascript://example.com/xss"