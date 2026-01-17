from requests.utils import get_auth_from_url

def test_get_auth_none():
    # urlparse(None) -> AttributeError (or TypeError in py3)
    # Caught by except (AttributeError, TypeError)
    assert get_auth_from_url(None) == ("", "")
