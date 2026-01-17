import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_https_to_http_standard():
    session = DummySession()
    # Downgrade on standard ports
    old = "https://example.com"
    new = "http://example.com"
    # Logic: changed_scheme=True. not (old port in default and new port in default) -> wait
    # old=https(443), new=http(80).
    # default_port lookup for old(https) is 443. old port is None(443). Match.
    # But code says:
    # if (not changed_scheme and ...): return False
    # So if changed_scheme is True, that block is skipped.
    # Returns changed_port or changed_scheme => True.
    
    # Wait, there is a special case before that:
    # if (old=http and old=80 and new=https and new=443): return False
    # But this is https -> http. So that doesn't apply.
    
    assert session.should_strip_auth(old, new) is True
