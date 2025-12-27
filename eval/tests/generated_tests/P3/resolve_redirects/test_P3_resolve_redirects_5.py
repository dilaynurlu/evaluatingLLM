import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_relative_url_and_fragment_preservation():
    """
    Test that relative redirect URLs are correctly resolved against the original URL,
    and that the URL fragment from the original request is preserved in the new request.
    """
    session = Session()
    
    # Original request with deep path and fragment
    req = PreparedRequest()
    req.prepare(method='GET', url="http://example.com/path/sub/original?q=1#section-a")
    
    # Response with relative redirect
    resp = Response()
    resp.status_code = 302
    resp.url = "http://example.com/path/sub/original?q=1"
    # Relative path using parent directory reference
    resp.headers['Location'] = "../../target" 
    resp._content = b""
    
    # Mock send
    session.send = MagicMock(return_value=Response())
    session.send.return_value._content = b""
    
    # Inspect the generated request
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    redirected_req = next(gen)
    
    # Verification logic:
    # Base: http://example.com/path/sub/original
    # Relative: ../../target
    # 1. Resolve relative: 
    #    /path/sub/original -> (dirname) /path/sub/
    #    /path/sub/ + ../../target -> /target
    #    Result: http://example.com/target
    # 2. Preserve fragment: #section-a
    
    assert redirected_req.url == "http://example.com/target#section-a"