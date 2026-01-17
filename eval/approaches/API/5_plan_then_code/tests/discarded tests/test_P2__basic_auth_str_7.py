import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error():
    """
    Test _basic_auth_str with string inputs containing characters NOT in Latin-1.
    Verifies that a UnicodeEncodeError is raised, as the function explicitly 
    encodes strings using 'latin1'.
    """
    # The snowman character \u2603 is not present in latin-1 encoding
    username = "user_with_☃"
    password = "password"

    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)