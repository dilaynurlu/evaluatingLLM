from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from unittest.mock import MagicMock

def test_HTTPDigestAuth_call_hooks():
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock a request object
    request = Request('GET', 'http://example.com')
    prepared_request = request.prepare()
    
    # Mock the register_hook method
    prepared_request.register_hook = MagicMock()
    
    # Call the auth object
    result = auth(prepared_request)
    
    # Verify hooks are registered
    assert prepared_request.register_hook.call_count == 2
    calls = prepared_request.register_hook.call_args_list
    
    # Expect (event, hook) tuples
    expected_hooks = [auth.handle_401, auth.handle_redirect]
    
    # Verify both 'response' hooks are registered with correct methods
    assert calls[0][0][0] == 'response'
    assert calls[0][0][1] in expected_hooks
    assert calls[1][0][0] == 'response'
    assert calls[1][0][1] in expected_hooks
    assert calls[0][0][1] != calls[1][0][1]
