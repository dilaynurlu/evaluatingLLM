import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import MagicMock

def test_resolve_redirects_protocol_relative_url_and_host_header():
    """
    Test handling of protocol-relative URLs (starting with //) and verification
    of Host header updates.
    """
    session = Session()
    
    # Request via HTTPS
    origin_host = "secure.example.com"
    target_host = "cdn.example.com"
    req = Request("GET", f"https://{origin_host}/resource").prepare()
    
    # Redirect with scheme-less location
    resp = Response()
    resp.request = req
    resp.url = f"https://{origin_host}/resource"
    resp.status_code = 302
    resp.headers["Location"] = f"//{target_host}/item"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=Response())
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    sent_req = session.send.call_args[0][0]
    
    # 1. Should resolve to https (inherited scheme)
    assert sent_req.url == f"https://{target_host}/item"
    
    # 2. Host header should be updated to the new target
    # Note: requests.prepare() handles Host header logic, but resolve_redirects 
    # must ensure the prepared request uses the new URL's host.
    assert sent_req.headers["Host"] == target_host