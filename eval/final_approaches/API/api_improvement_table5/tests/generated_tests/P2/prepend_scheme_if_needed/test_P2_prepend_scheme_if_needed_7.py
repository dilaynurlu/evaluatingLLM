import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_false_positive_scheme():
    """
    Test input that looks like it has a scheme (colon present at start), which the parser
    interprets as a scheme. The function should respect the parser's decision
    and NOT prepend the new scheme.
    """
    # 'user:pass@host' is technically a valid URI with scheme 'user'.
    url = "user:pass@example.com/foo"
    new_scheme = "http"
    
    # The function reconstructs the URL. Since a scheme is detected ('user'), 
    # 'http' is NOT added.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert not result.startswith("http://")
    assert result.startswith("user:")