import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    """
    Test _basic_auth_str with empty strings using static vectors.
    """
    username = ""
    password = ""
    
    # ":" -> Base64: Og==
    expected_auth_str = "Basic Og=="

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0

    assert result == expected_auth_str