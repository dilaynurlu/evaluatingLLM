from requests.utils import get_auth_from_url

def test_get_auth_from_url_none():
    # If no password provided (no colon), the function returns ('', '').
    url_no_pass = "http://user@example.com"
    auth1 = get_auth_from_url(url_no_pass)
    assert auth1 == ("", "")

    # No auth at all
    url_no_auth = "http://example.com"
    auth2 = get_auth_from_url(url_no_auth)
    assert auth2 == ("", "")
