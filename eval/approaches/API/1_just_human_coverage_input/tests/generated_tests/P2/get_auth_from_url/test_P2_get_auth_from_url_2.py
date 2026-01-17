from urllib.parse import quote
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction and decoding of credentials containing special characters
    that are percent-encoded in the URL.
    """
    # Characters like '@', ':', and '/' must be encoded in the userinfo section
    raw_user = "user@name"
    raw_pass = "pass/word:secret"
    
    # Encode with safe='' to ensure '/' is also encoded
    encoded_user = quote(raw_user, safe='')
    encoded_pass = quote(raw_pass, safe='')
    
    url = f"https://{encoded_user}:{encoded_pass}@example.com/api"
    
    # The function should unquote the extracted values
    assert get_auth_from_url(url) == (raw_user, raw_pass)