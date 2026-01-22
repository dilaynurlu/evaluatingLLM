from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import ChunkedEncodingError

def test_resolve_redirects_10():
    # Test consuming socket raises exception
    s = Session()
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "new"
    resp.url = "old"
    resp.request = PreparedRequest()
    resp.request.url = "old"
    resp.request.method = "GET"
    resp.request.headers = {}
    from requests.cookies import RequestsCookieJar
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    # Mock content access raising ChunkedEncodingError
    # Response.content accesses self._content. If it is False/None, it consumes raw.
    # We can mock resp.raw.read logic or better, mock resp.content property behavior if possible?
    # Or just let resp.raw.read raise it.
    # But wait, resp.content property catches RuntimeError etc? No.
    # resolve_redirects calls `resp.content` inside a try/except block catching ChunkedEncodingError.
    
    # We need to ensure `resp.content` call raises it.
    # `resp.content` calls `resp.iter_content` -> `generate`.
    
    # Easier: Mock the property `content` on the class? No, we have an instance.
    # We can't easily mock property on instance.
    # But `Response` code:
    # @property
    # def content(self):
    #    ... if self._content is False: self._content = b"".join(self.iter_content(...))
    
    # So if we make iter_content raise ChunkedEncodingError.
    
    def iter_content(*args, **kwargs):
        raise ChunkedEncodingError("fail")
        yield b""
        
    resp.iter_content = iter_content
    resp._content = False # Force consume
    
    # If resolve_redirects catches it, it should proceed to call resp.raw.read(decode_content=False)
    # We need to mock resp.raw.read too.
    
    class MockRaw2:
        def read(self, **kwargs): return b""
        def close(self): pass
    resp.raw = MockRaw2()
    
    gen = s.resolve_redirects(resp, resp.request, yield_requests=True)
    next(gen)
    # If it didn't crash, test passed.
