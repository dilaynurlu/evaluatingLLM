from requests.utils import get_auth_from_url

def test_get_auth_complex_pass():
    url = "http://user:p@ss:w@rd@example.com"
    # urlparse handles the last @ as the host separator, and the first : as user:pass separator?
    # Browsers might handle this differently. urlparse usually splits on last @.
    # user:p@ss:w@rd
    # username: user
    # password: p@ss:w@rd
    assert get_auth_from_url(url) == ("user", "p@ss:w@rd")
