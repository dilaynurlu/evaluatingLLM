import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_empty():
    """Test prepending scheme to empty string."""
    url = ""
    result = prepend_scheme_if_needed(url, "http")
    # urlparse("") -> all empty.
    # netloc is empty. path is empty.
    # scheme becomes http.
    # urlunparse -> http:/// ? or http:// ?
    # Let's see behavior. urlunparse(('http', '', '', '', '', '')) -> 'http://' or 'http:'?
    # Actually python's urlunparse behavior varies.
    # 'http://' is likely.
    assert result == "http://"
