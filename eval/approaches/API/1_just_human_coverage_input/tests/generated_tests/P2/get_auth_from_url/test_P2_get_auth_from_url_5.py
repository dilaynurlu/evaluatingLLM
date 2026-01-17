from requests.utils import get_auth_from_url

def test_get_auth_from_url_bytes_input():
    """
    Test that the function handles bytes input correctly and returns string components.
    """
    url = b"https://user:pass@example.com"
    expected = ("user", "pass")
    
    result = get_auth_from_url(url)
    
    assert result == expected
    # Ensure the return types are strings (decoded from bytes)
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)