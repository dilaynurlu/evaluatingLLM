import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_multiple_at_sign_ambiguity():
    """
    Test URLs containing multiple '@' characters.
    This checks the 'authority split' logic. Browsers and standard parsers
    typically treat the *last* '@' as the separator between userinfo and host.
    
    Input: user:pass@evil.com@example.com
    Expected: username='user', password='pass@evil.com'
    """
    url = "http://user:pass@evil.com@example.com/resource"
    # The parser should treat 'user:pass@evil.com' as the userinfo.
    # Therefore, password is 'pass@evil.com'.
    expected_auth = ("user", "pass@evil.com")
    
    assert get_auth_from_url(url) == expected_auth