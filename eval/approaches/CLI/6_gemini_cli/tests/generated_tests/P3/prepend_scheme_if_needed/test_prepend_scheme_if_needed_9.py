from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_just_path_segment():
    url = "foo"
    new_scheme = "http"
    # parse_url("foo") -> path="foo", netloc=None
    # swap -> netloc="foo", path=""
    # result -> http://foo
    assert prepend_scheme_if_needed(url, new_scheme) == "http://foo"
