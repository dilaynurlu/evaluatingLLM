from requests.auth import HTTPDigestAuth
from requests.models import Request

def test_HTTPDigestAuth_1():
    # Init
    auth = HTTPDigestAuth("user", "pass")
    assert auth.username == "user"
    assert auth.password == "pass"