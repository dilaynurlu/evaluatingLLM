import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_subdomain_change():
    session = DummySession()
    old = "http://sub1.example.com"
    new = "http://sub2.example.com"
    # Hostname changed
    assert session.should_strip_auth(old, new) is True
