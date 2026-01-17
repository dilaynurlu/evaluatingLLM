import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_host():
    """
    Test prepending a scheme to a simple hostname.
    Refined to include:
    1. Whitespace handling (leading/trailing).
    2. Host:Port ambiguity (e.g. localhost:8000).
    """
    scheme = "http"

    # Case 1: Simple host with whitespace
    url_ws = "  google.com  "
    expected_ws = "http://google.com"
    assert prepend_scheme_if_needed(url_ws, scheme) == expected_ws

    # Case 2: Host with port (often ambiguous in parsing)
    url_port = "localhost:8000"
    expected_port = "http://localhost:8000"
    assert prepend_scheme_if_needed(url_port, scheme) == expected_port