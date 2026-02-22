from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_1():
    url = "google.com"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "http://google.com"
