import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    Should correctly encode the string part to latin1 and join with the bytes part.
    """
    username = "user"
    password = b"pass"
    
    # Prepare expected value
    u_bytes = username.encode("latin1")
    p_bytes = password # already bytes
    raw_creds = b":".join((u_bytes, p_bytes))
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, f"Expected no warnings for mixed inputs, got: {[str(x.message) for x in w]}"

    assert result == expected_auth_str