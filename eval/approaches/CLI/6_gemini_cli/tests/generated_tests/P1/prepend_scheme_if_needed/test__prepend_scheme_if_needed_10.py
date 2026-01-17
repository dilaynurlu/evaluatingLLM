import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_fragment():
    url = "example.com#frag"
    new_url = prepend_scheme_if_needed(url, "https")
    assert new_url == "https://example.com#frag"
