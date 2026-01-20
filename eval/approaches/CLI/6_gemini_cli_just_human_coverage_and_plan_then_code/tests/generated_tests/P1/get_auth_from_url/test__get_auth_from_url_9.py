import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_user_only_implicitly_no_pass():
    # "http://user@example.com" -> parsed.password is None.
    # get_auth_from_url tries unquote(None) -> TypeError -> catch -> returns ("","")
    url = "http://user@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
