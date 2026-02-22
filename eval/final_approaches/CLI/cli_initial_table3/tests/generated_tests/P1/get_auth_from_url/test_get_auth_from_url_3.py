from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_components():
    # user only with colon, but empty pass
    url1 = "http://user:@example.com"
    auth1 = get_auth_from_url(url1)
    assert auth1 == ("user", "")
    
    # pass only, empty user
    url2 = "http://:pass@example.com"
    auth2 = get_auth_from_url(url2)
    assert auth2 == ("", "pass")
