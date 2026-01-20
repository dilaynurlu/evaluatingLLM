
import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_with_auth_no_scheme():
    # Defect in urlparse where netloc is missing sometimes if no scheme
    url = "user:pass@example.com"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://user:pass@example.com"
