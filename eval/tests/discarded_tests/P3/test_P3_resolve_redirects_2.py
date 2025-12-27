import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_strips_auth_on_cross_origin():
    """
    Test that the Authorization header is stripped when redirecting 
    to a different host (security check).
    Also verifies that the request history is maintained.
    """
    session = Session()
    
    # Initial Request with Sensitive Headers
    req = PreparedRequest()
    req.prepare(
        method='GET', 
        url="http://example.com/source", 
        headers={'Authorization': 'Basic secret123', 'User-Agent': 'test-agent'}
    )
    
    # First Response: Redirect to different host
    resp1 = Response()
    resp1.status_code = 301
    resp1.url = "http://example.com/source"
    resp1.headers['Location'] = "http://other-host.com/dest"
    resp1._content = b""
    
    # Second Response: Success (Target of redirect)
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = "http://other-host.com/dest"
    resp2._content = b""
    
    # Mock send to return the second response
    session.send = MagicMock(return_value=resp2)
    
    # Execute
    gen = session.resolve_redirects(resp1, req)
    history_results = list(gen)
    
    # Assertions on Flow
    assert len(history_results) == 1
    final_resp = history_results[0]
    assert final_resp == resp2
    
    # Verify Auth Header Stripping
    # Retrieve the request object that was passed to session.send()
    call_args = session.send.call_args
    assert call_args is not None
    redirected_request = call_args[0][0]
    
    assert redirected_request.url == "http://other-host.com/dest"
    assert 'Authorization' not in redirected_request.headers, "Authorization header leaked to cross-origin host"
    assert redirected_request.headers['User-Agent'] == 'test-agent', "Non-sensitive headers should be preserved"
    
    # Verify History
    # resolve_redirects populates the history of the response it yields
    assert len(final_resp.history) == 1
    assert final_resp.history[0] == resp1


'''
Execution failed:

 # Mock send to return the second response
        session.send = MagicMock(return_value=resp2)
    
        # Execute
        gen = session.resolve_redirects(resp1, req)
>       history_results = list(gen)
                          ^^^^^^^^^

eval/tests/generated_tests/P3/resolve_redirects/test_P3_resolve_redirects_2.py:40: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
requests/src/requests/sessions.py:246: in resolve_redirects
    self.rebuild_auth(prepared_request, resp)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <requests.sessions.Session object at 0xffff9b7f9110>
prepared_request = <PreparedRequest [GET]>, response = <Response [301]>

    def rebuild_auth(self, prepared_request, response):
        """When being redirected we may want to strip authentication from the
        request to avoid leaking credentials. This method intelligently removes
        and reapplies authentication where possible to avoid credential loss.
        """
        headers = prepared_request.headers
        url = prepared_request.url
    
        if "Authorization" in headers and self.should_strip_auth(
>           response.request.url, url
            ^^^^^^^^^^^^^^^^^^^^
        ):
E       AttributeError: 'NoneType' object has no attribute 'url'

requests/src/requests/sessions.py:291: AttributeError

'''