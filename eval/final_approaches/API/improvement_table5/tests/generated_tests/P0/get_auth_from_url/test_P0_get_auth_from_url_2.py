import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_percent_encoded_credentials():
    """
    Test extracting credentials that contain percent-encoded characters.
    The function should unquote (decode) the components.
    """
    # user -> "u$er", password -> "p@ssword"
    # $ is %24, @ is %40
    url = "http://u%24er:p%40ssword@example.com/"
    auth = get_auth_from_url(url)
    
    assert auth == ("u$er", "p@ssword")