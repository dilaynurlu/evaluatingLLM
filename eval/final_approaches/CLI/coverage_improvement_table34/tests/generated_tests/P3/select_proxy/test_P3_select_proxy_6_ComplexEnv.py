import pytest
import os
import requests
from requests.utils import resolve_proxies
from requests.models import PreparedRequest
from unittest.mock import patch

def test_resolve_proxies_complex_env():
    """
    Test resolve_proxies interaction with environment variables via get_environ_proxies
    and proxy_bypass logic.
    """
    env = {
        "http_proxy": "http://proxy.example.com",
        "no_proxy": "google.com, .example.com"
    }
    
    req = PreparedRequest()
    
    with patch.dict(os.environ, env):
        # 1. Should use proxy for non-bypassed
        req.url = "http://foo.com"
        proxies = resolve_proxies(req, None)
        assert proxies["http"] == "http://proxy.example.com"
        
        # 2. Should bypass for google.com
        # resolve_proxies returns merged dict. If bypassed, it might not be in it?
        # get_environ_proxies returns {} if bypassed.
        req.url = "http://google.com"
        proxies = resolve_proxies(req, None)
        assert "http" not in proxies
        
        # 3. Should bypass for subdomain of example.com
        req.url = "http://foo.example.com"
        proxies = resolve_proxies(req, None)
        assert "http" not in proxies
