import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_colon_in_password():
    # Colons in password must be encoded or they might be parsed as port separator or something else depending on parser
    # But strictly user:pass. If pass contains colon, it should be encoded if we want to be safe, 
    # but urlparse handles user:pass where pass has colon?
    # http://user:pass:word@host -> user is 'user', password is 'pass:word' ?
    # Let's test encoded colon first.
    url = "http://user:pass%3Aword@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pass:word")
