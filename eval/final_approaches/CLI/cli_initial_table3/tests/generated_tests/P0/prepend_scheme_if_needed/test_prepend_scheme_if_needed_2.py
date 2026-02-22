from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_2():
    url = "https://google.com"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "https://google.com"
