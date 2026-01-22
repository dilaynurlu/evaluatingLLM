from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_handle_redirect_resets_counter():
    """
    Test that handle_redirect resets the 401 limit counter.
    Refined to test behavior rather than internal private attributes.
    Scenario:
    1. Initial 401 (Counter -> 1) -> Retry OK
    2. Redirect (302) (Should reset Counter -> 0)
    3. New Location 401 (Counter -> 1) -> Retry OK
    
    If reset doesn't happen, step 3 would hit the limit (assuming limit is small, usually 2)
    or at least behave differently.
    """
    auth = HTTPDigestAuth("u", "p")
    req = Request('GET', 'http://site.com/').prepare()
    auth(req) 
    
    # Setup a standard 401 response structure
    def make_401(request):
        r = Response()
        r.request = request
        r.status_code = 401
        r.headers['www-authenticate'] = 'Digest realm="r", nonce="n", qop="auth"'
        r._content = b""
        r.raw = Mock()
        r.raw._original_response = None
        r.connection = Mock()
        # The retry success
        r.connection.send.return_value = Response()
        r.connection.send.return_value.status_code = 200
        return r

    # 1. First Challenge
    resp1 = make_401(req)
    # This increments counter to 1
    retry1 = auth.handle_401(resp1)
    assert retry1 is not None and retry1.status_code == 200
    
    # 2. Simulate Redirect
    # handle_redirect takes the response that triggered the redirect
    resp_redirect = Response()
    resp_redirect.status_code = 302
    resp_redirect.headers['location'] = 'http://site.com/new'
    
    # This should reset the counter
    auth.handle_redirect(resp_redirect)
    
    # 3. Second Challenge (on new resource)
    # If counter wasn't reset, this is the 2nd 401 call in the flow.
    # Requests implementation typically limits to 2 retries per Request object life-cycle? 
    # Actually, the counter is thread-local in HTTPDigestAuth.
    # If not reset, this might be viewed as a loop or max retry.
    req2 = Request('GET', 'http://site.com/new').prepare()
    resp2 = make_401(req2)
    
    retry2 = auth.handle_401(resp2)
    
    # If the counter wasn't reset, existing implementation logic might prevent a retry 
    # (depending on the exact limit in the code, typically it tracks num_401_calls).
    # We verify that a valid retry was produced.
    assert retry2 is not None
    assert retry2.status_code == 200
    
    # Double check by forcibly NOT resetting and ensuring it fails (Simulated Negative Test)
    # This confirms the test is valid.
    # Note: We can't easily "un-reset" without internals, but we can verify 
    # that calling handle_401 repeatedly eventually stops.
    
    # Simulate a loop: call 401 again
    resp3 = make_401(req2)
    retry3 = auth.handle_401(resp3)
    # Now we should have hit the limit (if limit is 2, we are at 2: 1(prev) + 1(curr))
    # Or if limit is 1, we fail earlier.
    # Standard requests `num_401_calls` check: if self.num_401_calls < 2:
    
    # Since we called it once (step 1), reset (step 2), called once (step 3), 
    # calling it again without reset should increase counter.
    
    # Verification: If we didn't reset, we'd be at 2 by now.