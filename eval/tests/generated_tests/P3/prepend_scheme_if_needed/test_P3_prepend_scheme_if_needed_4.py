from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_complex_and_scheme_like_inputs():
    """
    Test preservation of complex components and handling of inputs that
    resemble schemes (e.g., host:port) to ensure they are not mistaken for a scheme.
    """
    new_scheme = "http"

    # Case 1: Complex path, query, and fragment
    url_complex = "api.example.com/v1/resource?search=test#fragment"
    expected_complex = "http://api.example.com/v1/resource?search=test#fragment"
    assert prepend_scheme_if_needed(url_complex, new_scheme) == expected_complex

    # Case 2: "Scheme-like" input (host:port).
    # "example.com:80" could be misparsed as scheme="example.com", path="80".
    # The function should correctly identify this as missing a scheme.
    url_port = "example.com:80"
    expected_port = "http://example.com:80"
    assert prepend_scheme_if_needed(url_port, new_scheme) == expected_port