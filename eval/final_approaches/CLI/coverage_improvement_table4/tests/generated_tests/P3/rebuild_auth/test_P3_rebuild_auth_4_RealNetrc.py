import pytest
import os
import tempfile
from requests.sessions import SessionRedirectMixin
from requests.models import PreparedRequest, Response
from requests.utils import get_netrc_auth

def test_rebuild_auth_real_netrc():
    mixin = SessionRedirectMixin()
    mixin.trust_env = True
    
    req = PreparedRequest()
    req.url = "http://example.com/page1"
    req.headers = {}
    
    resp = Response() # Mock/Real
    # We need a response that triggers rebuild_auth logic if we call it directly?
    # Or just call rebuild_auth.
    # rebuild_auth checks if new_auth is not None.
    # new_auth = get_netrc_auth(url)
    
    # Setup netrc
    netrc_content = "machine other.com login user password pass"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(netrc_content)
        netrc_path = f.name
        
    try:
        os.environ["NETRC"] = netrc_path
        
        # Test get_netrc_auth directly first to ensure coverage there
        auth = get_netrc_auth("http://other.com/foo")
        assert auth == ("user", "pass")
        
        # Now test via rebuild_auth
        req.url = "http://other.com/login" # Destination URL
        # rebuild_auth(prepared_request, response)
        # It uses req.url for lookup.
        
        resp.request = PreparedRequest()
        resp.request.url = "http://example.com/old" # Old URL
        
        mixin.rebuild_auth(req, resp)
        
        assert "Authorization" in req.headers
        assert req.headers["Authorization"].startswith("Basic ")
        
    finally:
        if os.path.exists(netrc_path):
            os.remove(netrc_path)
        del os.environ["NETRC"]
