from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_double_slash():
    url = "//example.com"
    new_scheme = "http"
    # urlparse("//example.com") -> netloc="example.com", scheme=""
    assert prepend_scheme_if_needed(url, new_scheme) == "http://example.com"
