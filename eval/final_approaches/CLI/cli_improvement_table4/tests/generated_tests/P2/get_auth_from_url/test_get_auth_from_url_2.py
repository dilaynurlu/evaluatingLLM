from requests.utils import get_auth_from_url

def test_get_auth_encoded():
    # %40 is @, %3A is :
    url = "http://u%40ser:p%3Ass@example.com"
    assert get_auth_from_url(url) == ("u@ser", "p:ss")
