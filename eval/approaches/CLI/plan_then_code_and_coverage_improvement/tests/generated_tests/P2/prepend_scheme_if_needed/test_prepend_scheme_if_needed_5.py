from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_host_only():
    # "google.com" is parsed as path='google.com' by urlparse usually if scheme missing?
    # Actually requests.utils.parse_url handles this?
    # The function uses parse_url(url). 
    # If I pass "google.com", parse_url likely returns scheme=None, netloc='', path='google.com'.
    # The function swaps them.
    url = "google.com"
    assert prepend_scheme_if_needed(url, "http") == "http://google.com"
