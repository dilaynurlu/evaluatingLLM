import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_colon_in_creds():
    # Scenario: Username/Password contains colon
    # user:name : p:ssword
    # user:name:p:ssword -> dXNlcjpuYW1lOnA6c3N3b3Jk
    result = _basic_auth_str("user:name", "p:ssword")
    assert result == "Basic dXNlcjpuYW1lOnA6c3N3b3Jk"
