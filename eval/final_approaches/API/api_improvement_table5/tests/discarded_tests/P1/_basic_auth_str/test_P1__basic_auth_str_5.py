import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error():
    """
    Test _basic_auth_str with strings containing characters outside latin1.
    Verifies that a UnicodeEncodeError is raised, as the implementation 
    strictly attempts to encode strings using 'latin1'.
    """
    # The Euro sign '€' (\u20ac) is NOT in ISO-8859-1 (latin1).
    username = "user\u20ac"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)