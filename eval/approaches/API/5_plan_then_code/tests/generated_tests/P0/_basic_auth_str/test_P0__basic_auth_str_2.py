import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes inputs.
    Should handle bytes directly without latin1 encoding step (since they are already bytes)
    and produce valid header.
    """
    username = b"Aladdin"
    password = b"open sesame"
    
    # Prepare expected value locally
    # Bytes are used directly
    raw_creds = b":".join((username, password))
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, f"Expected no warnings for bytes inputs, got: {[str(x.message) for x in w]}"

    assert result == expected_auth_str