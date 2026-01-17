from requests.utils import get_auth_from_url

def test_get_auth_from_url_unicode_and_control_chars():
    """
    Test extraction of credentials containing:
    1. Percent-encoded Unicode characters (e.g., Emoji '☃' -> %E2%98%83).
    2. Percent-encoded control characters (e.g., Newline '\n' -> %0A).
    
    Refines coverage for:
    - Non-ASCII and Unicode Testing.
    - Handling of Sensitive Characters (CR/LF injection).
    """
    # user = "user☃" (Snowman), password = "pass\nword"
    url = "http://user%E2%98%83:pass%0Aword@example.com/resource"
    auth = get_auth_from_url(url)
    
    # Expected behavior: unquote decodes bytes to utf-8 string
    assert auth == ("user\u2603", "pass\nword")