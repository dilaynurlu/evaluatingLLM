import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_yield_requests():
    """
    Test that when yield_requests is True, the generator yields
    PreparedRequest objects instead of Response objects.
    """
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/start")
    
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "http://example.com/end"
    resp.url = "http://example.com/start"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    # Mock send, although strictly we yield before sending in this mode,
    # the function logic is: if yield_requests: yield req; else: send().
    # Wait, the logic is: 
    # if yield_requests: yield req 
    # else: send()...
    # BUT, the loop continues. If we yield req, do we continue?
    # The code is:
    # if yield_requests:
    #     yield req
    # else:
    #     resp = self.send(...)
    #
    # If we yield req, we pause. When resumed, it loops back? No.
    # It yields req. Then falls through? 
    # No, it's an if/else block.
    # If yield_requests is True, it yields 'req'.
    # Then it exits the if/else block.
    # Then it goes to top of loop? No, it's inside 'while url'.
    # If it yields 'req', it does NOT call self.send().
    # So 'resp' is NOT updated for the next iteration.
    # The 'url' variable is updated at the *bottom* of the else block? 
    # No, 'url' is updated via 'url = self.get_redirect_target(resp)' inside the ELSE block.
    #
    # If yield_requests is True:
    # 1. Update req.
    # 2. Yield req.
    # 3. Loop back.
    # But 'url' is still the OLD url (from previous iteration). It hasn't been updated because get_redirect_target wasn't called on a new response.
    # This would cause an infinite loop if 'url' isn't cleared.
    # However, 'resolve_redirects' is designed to be used by Session.send which handles the sending if yield_requests is True?
    # No, usually resolve_redirects is internal. 
    # Let's check the provided code carefully.
    
    # Code:
    # ...
    # req = prepared_request
    # if yield_requests:
    #     yield req
    # else:
    #     resp = self.send(...)
    #     url = self.get_redirect_target(resp)
    #     yield resp
    
    # If yield_requests is True, 'url' is NOT updated. 
    # The loop condition is 'while url:'.
    # If url remains truthy, it loops forever yielding the same request?
    # This implies 'yield_requests=True' expects the CALLER to handle sending and probably breaking the loop? 
    # Or maybe it's only intended for a single step?
    # Actually, looking at the code, if yield_requests is True, 'url' doesn't change.
    # This seems like it would loop infinitely if 'url' was valid.
    # UNLESS 'url' was modified inside the loop logic before this block?
    # 'url' is modified: 
    # 1. Start of loop: 'while url'.
    # 2. 'url' is used to build 'prepared_request'.
    # 3. Then 'url' is overwritten?
    #    "url = parsed.geturl()" (re-composed from redirect location)
    #    "prepared_request.url = ... url"
    # It does NOT reset 'url' to None or a new redirect target from a NEW response.
    # So 'url' remains the redirect target URL.
    # If we loop, we process the SAME redirect target again?
    # No, `resp.history` increases. Eventually `TooManyRedirects`.
    # BUT, `resp` is not updated if we don't call `send`. `resp` is the OLD response.
    # So `hist.append(resp)` appends the SAME response repeatedly.
    # So it yields the request, then loops, appends same resp, yields request... until max_redirects.
    # This seems to be the behavior for `yield_requests=True`. It generates the redirect request but doesn't follow it.
    # But wait, if it loops, it keeps generating requests for the SAME redirect?
    # Yes, because 'resp' hasn't changed.
    #
    # So the test should expect exactly one yielded request if we verify behavior for a single step, 
    # or expect it to crash if we iterate too much?
    # OR, maybe we should stop after 1.
    
    # Let's verify it yields a PreparedRequest object with the correct URL.
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    yielded_obj = next(gen)
    
    assert isinstance(yielded_obj, PreparedRequest)
    assert yielded_obj.url == "http://example.com/end"
    
    # We close the generator to avoid infinite loop logic in the test cleanup
    gen.close()