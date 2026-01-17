import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_strip_check():
    # Scenario: Ensure no whitespace at ends
    # b64encode output might not have whitespace usually, but .strip() is called.
    # We trust the library logic, just verifying output structure again.
    res = _basic_auth_str("user", "pass")
    assert res.strip() == res
