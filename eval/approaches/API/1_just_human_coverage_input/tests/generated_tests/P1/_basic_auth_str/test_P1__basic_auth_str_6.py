import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string_inputs_warning():
    username = 12345
    password = 67890
    
    # If inputs are not basestring (str/bytes), they are converted to str
    # and a DeprecationWarning is issued.
    user_str = str(username)
    pass_str = str(password)
    
    user_bytes = user_str.encode('latin1')
    pass_bytes = pass_str.encode('latin1')
    raw = b':'.join((user_bytes, pass_bytes))
    
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify warnings
        deprecation_warnings = [
            x for x in w if issubclass(x.category, DeprecationWarning)
        ]
        
        # We expect two warnings: one for username, one for password
        assert len(deprecation_warnings) == 2
        
        # Check messages contain context about the specific argument
        # Note: Implementation checks username first, then password
        assert "Non-string usernames" in str(deprecation_warnings[0].message)
        assert "Non-string passwords" in str(deprecation_warnings[1].message)
    
    assert result == expected