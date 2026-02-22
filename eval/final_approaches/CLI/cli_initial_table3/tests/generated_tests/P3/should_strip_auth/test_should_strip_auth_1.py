import pytest
from requests.sessions import SessionRedirectMixin

class MockMixin(SessionRedirectMixin):
    pass

def test_should_strip_auth_1():
    mixin = MockMixin()
    # Same host
    assert mixin.should_strip_auth("http://example.com/foo", "http://example.com/bar") is False

def test_should_strip_auth_2():
    mixin = MockMixin()
    # Different host
    assert mixin.should_strip_auth("http://example.com/foo", "http://other.com/bar") is True

def test_should_strip_auth_3():
    mixin = MockMixin()
    # http -> https upgrade
    assert mixin.should_strip_auth("http://example.com/foo", "https://example.com/bar") is False

def test_should_strip_auth_4():
    mixin = MockMixin()
    # https -> http downgrade (port change implicit)
    assert mixin.should_strip_auth("https://example.com/foo", "http://example.com/bar") is True
