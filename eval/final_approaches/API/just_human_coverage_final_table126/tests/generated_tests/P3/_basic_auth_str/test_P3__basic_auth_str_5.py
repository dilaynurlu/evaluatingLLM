import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_integers_deprecation():
    """
    Test _basic_auth_str with non-string inputs (Integers, None).
    Should emit DeprecationWarning and stringify the inputs.
    """
    # 1. Integers
    username = 12345
    password = 67890
    # "12345:67890" -> Base64: MTIzNDU6Njc4OTA=
    expected_int_auth = "Basic MTIzNDU6Njc4OTA="

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify result correctness
        assert result == expected_int_auth
        
        # Verify deprecation warnings
        assert len(w) >= 2
        messages = [str(warn.message) for warn in w]
        assert any("Non-string usernames" in msg for msg in messages)
        assert any("Non-string passwords" in msg for msg in messages)
        assert all(issubclass(warn.category, DeprecationWarning) for warn in w)

    # 2. None Type (Common runtime error source)
    # Should convert to string "None"
    # "None:None" -> Base64: Tm9uZTpOb25l
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result_none = _basic_auth_str(None, None)
        assert result_none == "Basic Tm9uZTpOb25l"
        assert len(w) >= 2