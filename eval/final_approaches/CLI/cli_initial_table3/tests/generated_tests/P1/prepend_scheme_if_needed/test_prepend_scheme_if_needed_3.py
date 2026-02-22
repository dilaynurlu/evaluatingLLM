from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_auth_port():
    # Auth and port but no scheme (start with // to avoid urlparse misinterpreting user as scheme)
    url = "//user:pass@example.com:8080/foo"
    new_scheme = "http"
    expected = "http://user:pass@example.com:8080/foo"
    assert prepend_scheme_if_needed(url, new_scheme) == expected

    # With scheme already
    url2 = "https://user:pass@example.com:8080"
    expected2 = "https://user:pass@example.com:8080"
    assert prepend_scheme_if_needed(url2, new_scheme) == expected2
