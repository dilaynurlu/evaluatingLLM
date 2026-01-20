from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_no_scheme_path_looks_like_host():
    url = "localhost/foo"
    new_scheme = "http"
    # localhost has no scheme.
    assert prepend_scheme_if_needed(url, new_scheme) == "http://localhost/foo"
