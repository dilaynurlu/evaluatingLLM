import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_empty_string():
    url = ""
    # if empty, urlparse returns empty everything.
    # netloc="", path=""
    # returns scheme:///
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://"
