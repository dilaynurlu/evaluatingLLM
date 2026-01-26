import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_empty():
    url = ""
    new_url = prepend_scheme_if_needed(url, "http")
    # Empty string is just path="", so it becomes "http:///".
    # Wait, "http://" + "" -> "http://" ?
    # Let's check logic:
    # scheme=None. netloc="". path="".
    # if scheme is None: scheme = "http".
    # urlunparse(("http", "", "", "", "", "")) -> "http://"
    # But wait, prepend_scheme_if_needed returns urlunparse.
    # If path is empty string...
    assert new_url == "http://"
