from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_auth():
    url = "user:pass@example.com"
    new_scheme = "http"
    # parse_url sees "user" as scheme, so no prepend happens
    assert prepend_scheme_if_needed(url, new_scheme) == "user:///pass@example.com"
