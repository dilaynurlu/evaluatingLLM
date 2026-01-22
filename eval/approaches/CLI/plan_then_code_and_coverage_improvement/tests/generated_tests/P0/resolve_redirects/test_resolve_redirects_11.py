from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import TooManyRedirects

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 1 # Exactly 1 allowed
        self.cookies = RequestsCookieJar()
        self.trust_env = False
        self.auth = None
        self.proxies = {}
        self.responses = []
    
    def send(self, request, **kwargs):
        resp = Response()
        resp.status_code = 301
        resp.headers["Location"] = "/next"
        resp.url = request.url
        resp.request = request
        resp._content = b""
        return resp
    
    def rebuild_proxies(self, r, p): return p

def test_resolve_redirects_11():
    # Test hitting max_redirects boundary
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 301
    r0.headers["Location"] = "/1"
    r0.request = Request("GET", "http://example.com/0").prepare()
    r0.url = "http://example.com/0"
    r0._content = b""
    
    # It should allow 1 redirect, then fail on the 2nd attempt?
    # resolve_redirects loop:
    # 1. yield request (if yield_requests) -> no
    # 2. send() -> gets redirect response
    # 3. check len(resp.history) < max_redirects
    
    # If we chain redirects:
    # Call 1: r0 (history []) -> sends -> gets r1 (history [r0]) -> len=1. max=1. 1 < 1 is False? No.
    # Code: if len(resp.history) >= self.max_redirects: raise
    # So if max=1, and we have 1 history item, we raise.
    
    # So 1 redirect means: Request -> 301 -> Request -> 200.
    # History of final response: [301]. len=1.
    
    # If we have endless loop:
    # r0 (hist=[])
    # Loop 1:
    #   send -> r1 (hist=[r0])
    #   len=1 >= 1 -> Raise!
    # Wait, if max_redirects=1, we expect 1 redirect to succeed.
    # But if checking >=, then 1 redirect fails?
    # Default is 30.
    
    try:
        list(session.resolve_redirects(r0, r0.request))
    except TooManyRedirects:
        # If it raises, it means 1 redirect was too many?
        # That seems wrong if max=1.
        # Let's see code:
        # hist.append(resp)
        # resp.history = hist[1:] 
        # ... 
        # if len(resp.history) >= self.max_redirects: raise
        
        # Start: r0. hist=[]. 
        # Loop 1: hist=[r0]. resp.history=[]. len=0.
        # send -> r1. 
        # Loop 2: r1. hist=[r0, r1]. resp.history=[r1]. len=1. 1 >= 1 -> Raise.
        
        # So resolve_redirects consumes the *next* redirect but checks limit *before* sending it?
        # No, the loop is `while url`.
        # r0 comes in. url derived from r0.
        # Loop 1: 
        #   hist starts empty? No, local var `hist = []`.
        #   hist.append(resp) -> [r0]
        #   resp.history = []
        #   ...
        #   send() -> returns r1.
        #   url = r1.headers['location']
        # Loop 2:
        #   resp is now r1.
        #   hist.append(r1) -> [r0, r1]
        #   resp.history = [r0] (wait, hist[1:]? No, hist is [r0, r1]. hist[1:] is [r1]?)
        #   Actually the code uses `hist` local var which accumulates.
        #   If r0 was the *first* response, it wasn't in any history.
        #   Wait, `resp` is the *current* response being handled.
        
        # Let's trace carefully.
        # r0 is passed in.
        # hist = []
        # Loop 1:
        #   hist.append(r0) -> [r0]
        #   r0.history = [] (slice 1:)
        #   ...
        #   send() -> returns r1.
        #   url from r1.
        # Loop 2:
        #   r1 is current.
        #   hist.append(r1) -> [r0, r1]
        #   r1.history = [r1] (slice 1:) -- Wait, hist is [r0, r1]. hist[1:] is [r1].
        #   check len(r1.history) >= max.
        #   1 >= 1 -> Raise.
        
        # So max_redirects=1 means "allow 1 hop"?
        # r0 -> r1. r1 is the result.
        # But if r1 is *also* a redirect, then we enter Loop 2 and crash.
        # If r1 is 200, url is None, loop terminates.
        
        # So: r0(301) -> r1(301) -> TooManyRedirects.
        pass
    
    # We want to test that it DOES raise if we go beyond.
    # Our mock always redirects.
    # So r0 -> r1(301) -> r2(301)...
    # With max=1, we expect failure when processing r1.
    
    try:
        list(session.resolve_redirects(r0, r0.request))
    except TooManyRedirects:
        pass
    else:
        assert False, "Should have raised TooManyRedirects"
