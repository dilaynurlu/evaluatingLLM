from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_simple_hostname_and_edge_cases():
    """
    Test prepending scheme to simple hostnames, including those with ports
    (which can be confused with schemes) and Internationalized Domain Names (IDN).
    Refines coverage for ambiguous hostnames and Unicode characters.
    """
    # Simple hostname
    url_simple = "google.com"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url_simple, new_scheme) == "http://google.com"

    # Ambiguous hostname with port (Critique: Port Confusion)
    # 'localhost' is not a valid scheme, so the function should prepend 'http'.
    url_with_port = "localhost:8080"
    assert prepend_scheme_if_needed(url_with_port, new_scheme) == "http://localhost:8080"

    # IDN / Unicode hostname (Critique: Internationalized Domain Names)
    url_idn = "bücher.ch"
    assert prepend_scheme_if_needed(url_idn, "https") == "https://bücher.ch"