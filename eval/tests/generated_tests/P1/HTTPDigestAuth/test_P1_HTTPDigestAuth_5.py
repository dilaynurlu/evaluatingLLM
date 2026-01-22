import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_rewind_body():
    """
    Test that the request body is rewound (using seek) before the request is re-sent
    upon a 401 challenge.
    """
    class MockBody:
        def __init__(self):
            self.pos = 0
            self.seek_log = []

        def tell(self):
            return self.pos

        def seek(self, pos, whence=0):
            self.pos = pos
            self.seek_log.append(pos)
        
        def read(self, size=-1):
            return b""

    url = "http://example.org/upload"
    auth = HTTPDigestAuth("user", "pass")
    body = MockBody()
    
    # Manually attach the body to the prepared request
    req = Request("POST", url, data=body).prepare()
    # Ensure our mock body replaces whatever prepare() did (if it didn't like the object)
    # But prepare() usually accepts objects with tell/read/seek.
    req.body = body
    
    # auth() call records the initial position via body.tell()
    # Let's say we are at 0
    auth(req)
    
    # Simulate partial read of body during first transmission (or just checking tell)
    # Move the cursor to simulate consumption
    body.pos = 50
    
    resp = Response()
    resp.status_code = 401
    resp.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth"'
    resp.url = url
    resp.request = req
    resp._content = b""
    resp.raw = Mock()
    resp.connection = Mock()
    
    success_resp = Response()
    success_resp.status_code = 200
    success_resp.history = []
    success_resp._content = b""
    resp.connection.send.return_value = success_resp
    
    # Trigger handle_401
    auth.handle_401(resp)
    
    # Verify seek was called with the original position (0)
    assert 0 in body.seek_log
    # Verify the request sent in the retry has the body
    sent_req = resp.connection.send.call_args[0][0]
    assert sent_req.body is body