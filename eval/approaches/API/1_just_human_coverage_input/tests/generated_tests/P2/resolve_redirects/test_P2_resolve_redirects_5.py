import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_relative_url_and_fragments():
    """
    Test handling of relative redirects (RFC 7231) and fragment behavior.
    If the redirect location has no fragment, the original fragment should be preserved.
    """
    session = Session()
    
    # URL has fragment
    req = Request('GET', 'http://example.com/path/old?q=1#frag').prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = 'http://example.com/path/old?q=1'
    # Relative redirect path, no fragment in location
    resp.headers = CaseInsensitiveDict({'Location': '../new'})
    resp.raw = MagicMock()
    
    final_resp = Response()
    final_resp.status_code = 200
    
    session.send = Mock(return_value=final_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    called_req = session.send.call_args[0][0]
    
    # Should resolve relative path: http://example.com/path/../new -> http://example.com/new
    # Should keep original fragment: #frag
    assert called_req.url == 'http://example.com/new#frag'