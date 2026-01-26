import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_to_http():
    mixin = SessionRedirectMixin()
    old = "https://example.com/old"
    new = "http://example.com/new"
    # Port change 443 -> 80, scheme change.
    # Logic:
    # if old.hostname != new.hostname: return True (False)
    # if old=http and new=https: return False (No)
    # changed_port = True (443 != 80)
    # changed_scheme = True
    # default_port = (None, None) for 'https'? No.
    # DEFAULT_PORTS = {'http': 80, 'https': 443}
    # default_port = (DEFAULT_PORTS.get('https'), None) -> (443, None)
    # if not changed_scheme ... (False)
    # return changed_port or changed_scheme -> True or True -> True
    
    assert mixin.should_strip_auth(old, new) is True
