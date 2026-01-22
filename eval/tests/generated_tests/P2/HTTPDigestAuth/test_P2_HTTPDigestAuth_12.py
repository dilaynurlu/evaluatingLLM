from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest

def test_auth_call_registers_hooks():
    # Scenario: Calling the auth object on a request should register response hooks
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com")
    
    # Apply auth
    auth(request)
    
    # Verify hooks are registered
    hooks = request.hooks["response"]
    assert auth.handle_401 in hooks
    assert auth.handle_redirect in hooks
    
    # Verify num_401_calls is initialized to 1
    assert auth._thread_local.num_401_calls == 1