from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_existing_scheme():
    url = "https://example.com"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "https://example.com"
