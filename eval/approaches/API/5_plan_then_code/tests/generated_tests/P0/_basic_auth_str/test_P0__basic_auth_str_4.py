import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_chars():
    """
    Test _basic_auth_str with non-ASCII characters that are valid in Latin-1 (ISO-8859-1).
    """
    # \u00a3 is Pound Sign, \u00a5 is Yen Sign. Both exist in Latin-1.
    username = "user\u00a3"
    password = "pass\u00a5"
    
    # Prepare expected value
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    raw_creds = b":".join((u_bytes, p_bytes))
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, f"Expected no warnings for latin1 inputs, got: {[str(x.message) for x in w]}"

    assert result == expected_auth_str