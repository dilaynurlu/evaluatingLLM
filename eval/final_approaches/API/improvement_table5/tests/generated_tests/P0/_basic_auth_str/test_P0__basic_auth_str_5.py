import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_username():
    """
    Test non-string/non-bytes username input (e.g. int).
    Should trigger a DeprecationWarning and convert the input to string.
    """
    username = 123456
    password = "password"
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify warning
        assert len(w) > 0
        assert issubclass(w[0].category, DeprecationWarning)
        assert "Non-string usernames" in str(w[0].message)
        
    # Verify the result uses the string representation of the int
    username_str = str(username)
    joined = (username_str + ":" + password).encode("latin1")
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    assert result == expected