import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_decodes_percent_encoded_credentials():
    """
    Test that get_auth_from_url correctly unquotes (decodes) percent-encoded
    characters in the username and password fields.
    
    Refinements:
    - Uses HTTPS.
    - Validates correct decoding of characters often found in credentials (@, /).
    - Masks output on failure.
    """
    # Encoded values: %40 -> @, %2F -> /
    # These represent complex credentials that require proper parsing
    encoded_part = "user%40email.com:pass%2Fword"
    url = f"https://{encoded_part}@example.com/api"
    
    expected_auth = ("user@email.com", "pass/word")
    actual_auth = get_auth_from_url(url)
    
    if actual_auth != expected_auth:
        raise AssertionError("Failed to decode percent-encoded credentials correctly. (Values hidden for security)")
    

'''
Manually marked as assertion correct in csv, because test contains a custom assertion. Justnot recognized by the tool
'''