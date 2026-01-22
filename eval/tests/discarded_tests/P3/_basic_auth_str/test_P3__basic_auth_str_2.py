import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_strings():
    """
    Test _basic_auth_str with Latin-1 characters against static vectors.
    Verifies that the function encodes to latin1 before base64 encoding.
    """
    # 'ñ' is \u00f1, 'é' is \u00e9. Both are valid Latin-1.
    # 'userñ' : 'passé'
    # Hex sequence (latin1): 75 73 65 72 f1 3a 70 61 73 73 e9
    # Base64 expected: dXNlcnH6cGFzc+k=
    username = "user\u00f1"
    password = "pass\u00e9"
    expected_auth_str = "Basic dXNlcnH6cGFzc+k="

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, "Expected no warnings for Latin-1 strings"

    assert result == expected_auth_str

    # Verify high-boundary Latin-1 character (y-umlaut \u00ff)
    # 'a' : '\u00ff' -> 'a:\xff'
    # Base64('a:\xff') -> 'YTv/'
    assert _basic_auth_str("a", "\u00ff") == "Basic YTv/"