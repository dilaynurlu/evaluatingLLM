import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_ints():
    """
    Test _basic_auth_str with integer inputs.
    This functionality is deprecated and should emit DeprecationWarning,
    while converting ints to strings and returning a valid Basic Auth header.
    """
    username = 12345
    password = 67890
    
    # Expected behavior: ints converted to strings, then encoded to latin1
    u_bytes = str(username).encode("latin1")
    p_bytes = str(password).encode("latin1")
    raw_creds = b":".join((u_bytes, p_bytes))
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify warnings
        assert len(w) >= 1, "Expected DeprecationWarning for int inputs"
        assert any(issubclass(x.category, DeprecationWarning) for x in w)
        messages = [str(x.message) for x in w]
        assert any("Non-string usernames" in msg for msg in messages)
        assert any("Non-string passwords" in msg for msg in messages)

    assert result == expected_auth_str