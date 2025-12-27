import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_initialization_and_hook_registration():
    """
    Test that calling the auth object on a request initializes thread-local state
    and registers the necessary hooks.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock a PreparedRequest object
    request = Mock()
    request.headers = {}
    request.body = None
    # Mock register_hook to capture calls
    request.register_hook = Mock()
    
    # Act
    returned_request = auth(request)
    
    # Assert
    assert returned_request is request
    
    # Check thread local initialization
    assert hasattr(auth._thread_local, "init")
    assert auth._thread_local.init is True
    assert auth._thread_local.last_nonce == ""
    assert auth._thread_local.nonce_count == 0
    assert auth._thread_local.chal == {}
    
    # Verify hooks registration
    # Expected: register_hook called twice (response: handle_401, response: handle_redirect)
    assert request.register_hook.call_count == 2
    
    calls = request.register_hook.call_args_list
    # Note: Order of registration depends on implementation, but typically sequential
    events = [args[0][0] for args in calls]
    hooks = [args[0][1] for args in calls]
    
    assert events == ["response", "response"]
    assert auth.handle_401 in hooks
    assert auth.handle_redirect in hooks