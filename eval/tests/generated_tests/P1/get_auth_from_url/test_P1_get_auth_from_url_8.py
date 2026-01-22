from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid_input_none():
    """
    Test that passing None handles the resulting AttributeError/TypeError gracefully
    and returns empty strings.
    """
    url = None
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth