import base64
import warnings
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes inputs.
    Verifies that bytes are accepted without modification/encoding, 
    no warnings are issued, and the result is correctly formatted.
    """
    username = b"user"
    password = b"pass123"

    # When inputs are bytes, they are used directly.
    raw = b":".join((username, password))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    # Ensure no DeprecationWarning is emitted for bytes (basestring includes bytes)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Cause all warnings to always be triggered.
        result = _basic_auth_str(username, password)
        
        # Filter for DeprecationWarning specifically related to requests if needed,
        # but here we just check no DeprecationWarning occurred.
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0, "Bytes input should not trigger DeprecationWarning"

    assert result == expected_auth_str