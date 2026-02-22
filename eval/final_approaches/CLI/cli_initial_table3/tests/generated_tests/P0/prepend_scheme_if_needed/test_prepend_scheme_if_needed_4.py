from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_4():
    url = ""
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "http://"
