from requests.utils import get_auth_from_url

def test_get_auth_only_user():
    url = "http://user@example.com"
    # password should be None in urlparse, unquote(None) -> TypeError -> caught -> returns ("", "")?
    # Wait, urlparse("http://user@example.com").password is None.
    # unquote(None) raises TypeError.
    # So it returns ("", "").
    # BUT wait, if I have user but no password, I expect ("user", None) or ("user", "")?
    # urlparse("http://user@example.com") -> username='user', password=None.
    # unquote('user') -> 'user'. unquote(None) -> TypeError.
    # Exception caught -> returns ("", ""). 
    # This seems like a bug or feature in requests. It returns ("", "") if ANY part fails.
    # Let's verify this behavior with the test.
    assert get_auth_from_url(url) == ("", "")
