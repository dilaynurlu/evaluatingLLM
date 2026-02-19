import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_both_deprecation():
    """
    Test scenario where both username and password are non-string objects.
    Should trigger warnings for both and convert both to strings.
    """
    username = 999
    password = 888
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Should have at least 2 warnings (one for each argument)
        assert len(w) >= 2
        messages = [str(x.message) for x in w]
        assert any("Non-string usernames" in m for m in messages)
        assert any("Non-string passwords" in m for m in messages)
        
    joined = b"999:888"
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    assert result == expected