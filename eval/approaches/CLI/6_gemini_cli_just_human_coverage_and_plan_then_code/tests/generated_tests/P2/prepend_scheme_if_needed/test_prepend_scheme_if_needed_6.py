import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_scheme_like_no_colon():
    # "google" looks like scheme "google" if parsed? No, needs colon.
    url = "google"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://google"
