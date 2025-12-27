import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_credentials():
    """
    Test _basic_auth_str with bytes input.
    Refined to include control characters and verify by decoding.
    """
    # Include control characters (newline, null) to ensure no stripping occurs
    test_user = b"byte_user\n"
    test_pass = b"byte_pass\x00"
    
    result = _basic_auth_str(test_user, test_pass)
    
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    decoded_bytes = base64.b64decode(token)
    
    # When inputs are bytes, they are joined directly with b':'
    expected_bytes = test_user + b":" + test_pass
    
    assert decoded_bytes == expected_bytes