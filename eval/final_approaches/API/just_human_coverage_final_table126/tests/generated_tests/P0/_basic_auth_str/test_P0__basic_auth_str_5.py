import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_ints():
    # Test that non-string/bytes inputs trigger DeprecationWarning and are converted to str
    username = 123
    password = 456
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Filter for relevant DeprecationWarnings
        dep_warnings = [
            x for x in w 
            if issubclass(x.category, DeprecationWarning) and "Non-string" in str(x.message)
        ]
        
        # We expect two warnings: one for username, one for password
        assert len(dep_warnings) >= 2
        assert "usernames" in str(dep_warnings[0].message) or "usernames" in str(dep_warnings[1].message)
        assert "passwords" in str(dep_warnings[0].message) or "passwords" in str(dep_warnings[1].message)

    # Expected calculation: inputs converted to str, then treated as standard strings
    raw_creds = (str(username) + ":" + str(password)).encode("latin1")
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert result == expected