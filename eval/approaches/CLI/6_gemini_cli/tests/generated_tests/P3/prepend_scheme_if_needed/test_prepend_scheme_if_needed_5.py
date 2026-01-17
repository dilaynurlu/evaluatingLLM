from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_empty():
    url = ""
    new_scheme = "http"
    # parse_url("") -> everything None or empty.
    # netloc="", path=""
    # Returns scheme://
    assert prepend_scheme_if_needed(url, new_scheme) == "http://"
