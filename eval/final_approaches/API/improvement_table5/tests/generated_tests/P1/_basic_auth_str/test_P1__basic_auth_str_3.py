import base64
import pytest
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_non_basestring():
    """
    Test _basic_auth_str with non-string/non-bytes arguments (e.g., integers).
    Verifies that DeprecationWarning is emitted for non-string inputs,
    values are converted to strings, and then processed correctly.
    """
    username = 12345
    password = 67890
    
    # Expected behavior:
    # 1. Warn about deprecation
    # 2. Convert to str -> "12345", "67890"
    # 3. Encode "12345" and "67890" to latin1
    # 4. Join and base64 encode
    
    expected_user = str(username).encode("latin1")
    expected_pass = str(password).encode("latin1")
    raw_credentials = expected_user + b":" + expected_pass
    encoded_credentials = base64.b64encode(raw_credentials).decode("ascii")
    expected_auth_str = f"Basic {encoded_credentials}"
    
    # We expect at least one DeprecationWarning (likely two, one for each arg)
    with pytest.warns(DeprecationWarning) as record:
        result = _basic_auth_str(username, password)
    
    # Assert checks
    assert len(record) >= 1, "Should emit DeprecationWarning for non-string inputs"
    assert result == expected_auth_str