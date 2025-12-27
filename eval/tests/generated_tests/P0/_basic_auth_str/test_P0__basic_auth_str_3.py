import pytest
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string_deprecation():
    """
    Test that providing non-string (and non-bytes) arguments (like integers)
    triggers a DeprecationWarning and correctly converts them to strings before encoding.
    """
    username = 123
    password = 456
    
    # Expected conversion: 123 -> "123", 456 -> "456"
    # "123:456" -> base64 -> "MTIzOjQ1Ng=="
    expected = "Basic MTIzOjQ1Ng=="
    
    with pytest.warns(DeprecationWarning) as record:
        result = _basic_auth_str(username, password)
        
    assert result == expected
    
    # Validate warnings were raised
    # Expect 2 warnings (one for username, one for password)
    assert len(record) >= 1
    messages = [str(w.message) for w in record]
    assert any("Non-string usernames" in m for m in messages)
    assert any("Non-string passwords" in m for m in messages)