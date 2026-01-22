import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input():
    """
    Test _basic_auth_str with bytes input using static vectors.
    Bytes should be joined directly without encoding conversion.
    """
    username = b"test_user"
    password = b"test_password"
    
    # b"test_user:test_password"
    # Base64: dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=
    expected_auth_str = "Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ="

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, "Expected no warnings for bytes input"

    assert result == expected_auth_str