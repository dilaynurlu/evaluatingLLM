from requests.utils import get_auth_from_url

def test_get_auth_from_url_4():
    url = "http://us%40er:pa%3Ass@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("us@er", "pa:ss")
