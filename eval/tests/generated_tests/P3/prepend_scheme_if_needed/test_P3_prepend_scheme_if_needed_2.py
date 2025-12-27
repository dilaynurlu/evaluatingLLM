from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_skips_existing_and_handles_protocol_relative():
    """
    Test that the function does not overwrite an existing scheme.
    Refined to include protocol-relative URLs (//) handling.
    """
    new_scheme = "http"

    # Case 1: Existing absolute scheme
    url_secure = "https://example.com"
    assert prepend_scheme_if_needed(url_secure, new_scheme) == "https://example.com"

    # Case 2: Protocol-relative URL (starting with //)
    # The parser typically identifies the netloc but no scheme.
    # The function should prepend the default scheme.
    url_relative = "//example.com"
    expected_relative = "http://example.com"
    assert prepend_scheme_if_needed(url_relative, new_scheme) == expected_relative