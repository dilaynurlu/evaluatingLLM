from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_4():
    # Test equality
    auth1 = HTTPDigestAuth("user", "pass")
    auth2 = HTTPDigestAuth("user", "pass")
    auth3 = HTTPDigestAuth("other", "pass")
    
    assert auth1 == auth2
    assert auth1 != auth3
