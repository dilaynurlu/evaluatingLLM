from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_rebuild_auth_1():
    # rebuild_auth: strip auth on redirect to new host
    s = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {}
    req.headers["Authorization"] = "Basic secret"
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://original.com/foo"
    # redirecting from original to example?
    # Wait, rebuild_auth(prepared_request, response)
    # prepared_request is the NEW request (to example.com)
    # response is the previous response (from original.com)
    
    # The logic:
    # if "Authorization" in headers and self.should_strip_auth(response.request.url, url):
    #    del headers["Authorization"]
    
    # So if response.request.url was "http://original.com"
    # and req.url is "http://example.com"
    # It should strip.
    
    s.rebuild_auth(req, resp)
    assert "Authorization" not in req.headers