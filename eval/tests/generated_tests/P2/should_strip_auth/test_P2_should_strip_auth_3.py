import requests

def test_should_keep_auth_on_secure_upgrade_standard_ports():
    """
    Test that Authorization headers are PRESERVED (not stripped) when upgrading
    from HTTP to HTTPS using standard ports (80 and 443/None).
    """
    session = requests.Session()
    # Explicit port 80 to implicit port 443 (via https scheme)
    old_url = "http://example.com:80/login"
    new_url = "https://example.com/login"
    
    # This falls under the special backward-compatibility case in requests
    assert session.should_strip_auth(old_url, new_url) is False