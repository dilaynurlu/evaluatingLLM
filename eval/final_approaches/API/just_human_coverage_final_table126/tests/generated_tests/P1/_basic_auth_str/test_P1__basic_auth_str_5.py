import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_integers_deprecation():
    """
    Test that passing non-string/non-bytes objects (like ints) triggers a DeprecationWarning
    and correctly converts the inputs to strings.
    """
    username = 123
    password = 456
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Filter for DeprecationWarning specifically
        dep_warnings = [
            x for x in w 
            if issubclass(x.category, DeprecationWarning) and "Non-string" in str(x.message)
        ]
        
        # Should have at least one warning (implementation emits one per invalid arg)
        assert len(dep_warnings) >= 2
    
    # Logic: ints are converted to str, then treated as strings (latin1 encoded)
    raw_payload = f"{username}:{password}".encode("latin1")
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected