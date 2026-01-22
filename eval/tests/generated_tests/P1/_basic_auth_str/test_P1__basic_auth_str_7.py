import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_none_deprecation():
    """
    Test that passing None triggers a DeprecationWarning and converts None to 'None'.
    """
    username = "user"
    password = None
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        dep_warnings = [
            x for x in w 
            if issubclass(x.category, DeprecationWarning) and "Non-string passwords" in str(x.message)
        ]
        assert len(dep_warnings) == 1
        
    # 'None' (str) is used
    raw_payload = f"{username}:{password}".encode("latin1")
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected