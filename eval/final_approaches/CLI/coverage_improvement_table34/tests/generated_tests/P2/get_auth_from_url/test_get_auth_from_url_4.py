from requests.utils import get_auth_from_url

def test_get_auth_partial():
    # user only, no colon -> password is None -> TypeError -> ("", "")
    url1 = "http://user@example.com"
    assert get_auth_from_url(url1) == ("", "")
    
    # user with colon -> password is "" -> ("", "") wait
    # unquote("") is "". ('user', '')
    url2 = "http://user:@example.com"
    assert get_auth_from_url(url2) == ("user", "")
