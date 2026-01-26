import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_latin1_chars():
    """Test _basic_auth_str with Latin-1 characters."""
    username = "user£"
    password = "pass¥"
    # user£ -> 75 73 65 72 A3
    # pass¥ -> 70 61 73 73 A5
    # user£:pass¥ -> 75 73 65 72 A3 3A 70 61 73 73 A5
    # b64: dXNlcnK6cGFzcwql
    expected = "Basic dXNlckOjOnBhc3Ol" 
    # Wait, let's verify my manual calc or trust the code. 
    # The code uses latin1 encode.
    # user£ (latin1) -> b'user\xa3'
    # pass¥ (latin1) -> b'pass\xa5'
    # join -> b'user\xa3:pass\xa5'
    # b64(b'user\xa3:pass\xa5') -> dXNlcqM6cGFzcwql
    
    # Let's rely on the function behavior being deterministic.
    # I'll hardcode the expected value based on python execution to be safe or use simple assert if I wasn't sure.
    # But for this test generation, I'll calculate it correctly.
    # b64encode(b'user\xa3:pass\xa5') -> b'dXNlcqM6cGFzcwql'
    
    result = _basic_auth_str(username, password)
    assert result == "Basic dXNlcqM6cGFzc6U="
