from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_3():
    # google.com/foo -> scheme=None
    url = "google.com/foo"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "http://google.com/foo"