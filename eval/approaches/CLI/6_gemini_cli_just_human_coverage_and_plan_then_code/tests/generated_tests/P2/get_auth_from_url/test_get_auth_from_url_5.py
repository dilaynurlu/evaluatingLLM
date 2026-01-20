import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid():
    # Scenario: url is None. urlparse(None) might fail or return weirdness.
    # If urlparse raises AttributeError/TypeError, function returns ('', '')
    
    # Actually urlparse(None) raises AttributeError in some versions or TypeError.
    # The function catches AttributeError, TypeError.
    auth = get_auth_from_url(None)
    assert auth == ("", "")
