import pytest
import requests
import os
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock, patch

def test_resolve_redirects_with_proxies_and_env():
    # Use a real session to trigger rebuild_proxies -> resolve_proxies -> get_environ_proxies
    session = requests.Session()
    session.trust_env = True
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.url = "http://example.com/old"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    resp.history = []
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.headers = {}
    new_resp.raw = Mock()
    new_resp.raw.headers = {}
    session.send = Mock(return_value=new_resp)
    
    # Define proxies
    proxies = {
        "http": "http://10.10.1.10:3128",
        "https": "http://10.10.1.10:1080",
    }
    
    # Mock environment variables to ensure get_environ_proxies does something
    # and should_bypass_proxies checks things.
    with patch.dict(os.environ, {"no_proxy": "localhost,127.0.0.1"}):
        # We pass the proxies argument to resolve_redirects
        gen = session.resolve_redirects(resp, req, proxies=proxies)
        next(gen)
    
    # Verify session.send was called with updated proxies
    args, kwargs = session.send.call_args
    # rebuild_proxies should have processed the proxies
    assert "proxies" in kwargs
    assert kwargs["proxies"]["http"] == "http://10.10.1.10:3128"
