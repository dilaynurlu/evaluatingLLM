from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_input_robustness():
    """
    Test preservation of path/query/fragment and robustness against edge case inputs
    like whitespace and empty strings.
    """
    new_scheme = "https"

    # Complex URL parts preservation
    url_complex = "api.example.org/v1/items?sort=desc&limit=10#top"
    assert prepend_scheme_if_needed(url_complex, new_scheme) == "https://api.example.org/v1/items?sort=desc&limit=10#top"

    # Leading whitespace (Critique: Leading/Trailing Whitespace)
    # The function typically prepends to the string as-is if no scheme is found.
    # This test verifies that the scheme is applied even if the URL is malformed with spaces.
    url_space = "   example.com"
    assert prepend_scheme_if_needed(url_space, new_scheme) == "https://   example.com"

    # Empty string input (Critique: Empty and Non-String Inputs)
    # Should result in just the scheme being returned (e.g. "https://")
    url_empty = ""
    assert prepend_scheme_if_needed(url_empty, new_scheme) == "https://"