from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_behavior_and_whitespace():
    """
    Test that a scheme is correctly prepended to a host-only URL.
    Refined to include whitespace handling checks as per critique.
    """
    # Standard case
    url = "google.com"
    new_scheme = "http"
    expected = "http://google.com"
    assert prepend_scheme_if_needed(url, new_scheme) == expected

    # Whitespace handling: The function should blindly prepend without crashing,
    # effectively preserving the whitespace in the netloc/path if the parser allows it.
    # We verify that the scheme is attached even if input is messy.
    messy_url = "  google.com  "
    result = prepend_scheme_if_needed(messy_url, new_scheme)
    assert result.strip() == "http://  google.com"