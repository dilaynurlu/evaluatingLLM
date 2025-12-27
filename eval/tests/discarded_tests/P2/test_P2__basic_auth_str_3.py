import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_special_characters():
    """
    Test _basic_auth_str with Latin-1 specific characters.
    The function encodes strings to 'latin1' before base64 encoding.
    """
    # 'ñ' is \xf1, 'ü' is \xfc in Latin-1
    username = "señor"
    password = "müller"
    
    # String "señor:müller"
    # Latin1 bytes: b'se\xf1or:m\xfcller'
    # Base64 encoded: b'c2Xxb3I6bcxlbGVy'
    expected_auth_str = "Basic c2Xxb3I6bcxlbGVy"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str

'''
Assertion failed:

# Base64 encoded: b'c2Xxb3I6bcxlbGVy'
        expected_auth_str = "Basic c2Xxb3I6bcxlbGVy"
    
        result = _basic_auth_str(username, password)
    
>       assert result == expected_auth_str
E       AssertionError: assert 'Basic c2Xxb3I6bfxsbGVy' == 'Basic c2Xxb3I6bcxlbGVy'
E         
E         - Basic c2Xxb3I6bcxlbGVy
E         ?                ^ ^
E         + Basic c2Xxb3I6bfxsbGVy
E         ?                ^ ^

eval/tests/generated_tests/P2/_basic_auth_str/test_P2__basic_auth_str_3.py:20: AssertionError
'''