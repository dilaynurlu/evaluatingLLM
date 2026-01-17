import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_leading_whitespace():
    url = " google.com" # Space at start prevents scheme detection
    new_url = prepend_scheme_if_needed(url, "http")
    # urlparse(" google.com") might be weird.
    # usually it treats as path.
    assert new_url == "http:// google.com"
