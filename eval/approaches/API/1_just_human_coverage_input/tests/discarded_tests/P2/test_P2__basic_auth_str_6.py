import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_raises_on_non_latin1():
    """
    Test _basic_auth_str with strings containing characters NOT present in Latin-1.
    Verifies that a UnicodeEncodeError is raised, as the implementation strictly 
    uses .encode('latin1') for string inputs.
    """
    # The snowman character '☃' (U+2603) is not valid in Latin-1.
    username = "Snowman"
    password = "☃" 

    # We expect the encoding step to fail
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)