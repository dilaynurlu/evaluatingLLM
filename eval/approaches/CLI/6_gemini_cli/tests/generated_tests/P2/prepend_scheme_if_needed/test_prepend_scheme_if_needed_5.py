import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_path_only():
    # If just "foo/bar", urlparse thinks it's path.
    # prepend_scheme should make it "http://foo/bar" ?
    # Let's check logic:
    # parsed.netloc is empty, path="foo/bar".
    # if not netloc: netloc, path = path, netloc -> netloc="foo/bar", path=""
    # scheme=new_scheme
    # returns scheme://netloc... -> http://foo/bar
    url = "foo/bar"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://foo/bar"
