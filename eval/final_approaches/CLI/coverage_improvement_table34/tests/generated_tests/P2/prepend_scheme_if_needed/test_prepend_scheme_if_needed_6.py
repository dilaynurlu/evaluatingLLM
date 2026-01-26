from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_empty():
    url = ""
    # parse_url("") -> scheme=None, netloc='', path=''
    # swap? no.
    # returns "http://"
    assert prepend_scheme_if_needed(url, "http") == "http://"
