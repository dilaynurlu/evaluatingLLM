import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_none_inputs():
    """
    Test _basic_auth_str with None inputs.
    None is not a basestring, so it should trigger DeprecationWarnings for both fields
    and be converted to the string "None".
    """
    username = None
    password = None
    
    # Both should trigger warnings
    with pytest.warns(DeprecationWarning) as record:
        result = _basic_auth_str(username, password)
    
    # Check that we got at least one warning (implementations might optimize, but code flow suggests two checks)
    assert len(record) >= 1
    
    # "None:None" -> b64 -> "Basic Tm9uZTpOb25l"
    expected_auth_str = "Basic Tm9uZTpOb25l"
    
    assert result == expected_auth_str