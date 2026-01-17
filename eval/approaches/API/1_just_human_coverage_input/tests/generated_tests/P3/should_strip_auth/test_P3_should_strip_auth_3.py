import requests
from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization header is stripped when downgrading from HTTPS to HTTP.
    This includes explicit port definitions that result in a scheme downgrade.
    """
    session = Session()
    
    # Standard downgrade
    assert session.should_strip_auth("https://example.com/secure", "http://example.com/secure") is True
    
    # Downgrade from explicit HTTPS port to implicit HTTP
    assert session.should_strip_auth("https://example.com:443/secure", "http://example.com/secure") is True
    
    # Downgrade from implicit HTTPS to explicit HTTP port
    assert session.should_strip_auth("https://example.com/secure", "http://example.com:80/secure") is True