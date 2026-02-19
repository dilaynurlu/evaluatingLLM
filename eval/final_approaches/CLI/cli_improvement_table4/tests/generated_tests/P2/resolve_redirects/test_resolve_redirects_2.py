from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_none():
    session = Session()
    
    resp = Response()
    resp.status_code = 200 # Not a redirect
    resp.url = "http://example.com"
    
    req = PreparedRequest()
    req.url = "http://example.com"
    
    gen = session.resolve_redirects(resp, req)
    assert list(gen) == []
