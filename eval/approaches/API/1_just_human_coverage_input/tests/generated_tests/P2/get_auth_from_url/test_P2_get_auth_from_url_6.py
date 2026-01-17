from requests.utils import get_auth_from_url

def test_get_auth_from_url_none_input():
    """
    Test that passing None instead of a URL string is handled gracefully
    (returning empty strings instead of raising TypeError/AttributeError).
    """
    assert get_auth_from_url(None) == ("", "")