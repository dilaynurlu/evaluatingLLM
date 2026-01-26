import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_path_swap_logic():
    """
    Test the specific branch where 'netloc' is missing but 'path' is present.
    This triggers a legacy fixup in the function that swaps path and netloc.
    
    Input starting with '/' (e.g., '/foo') matches the scheme regex of parse_url
    (preventing implicit '//' prepending) but fails to parse as a scheme,
    resulting in the entire string being treated as a path.
    """
    url = "/foo"
    new_scheme = "http"
    
    # Logic:
    # 1. parse_url("/foo") -> scheme=None, netloc=None, path="/foo"
    # 2. if not netloc: swap -> netloc="/foo", path=None
    # 3. scheme="http"
    # 4. urlunparse -> http:///foo (scheme://netloc/path)
    expected = "http:///foo"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected