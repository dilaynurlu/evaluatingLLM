import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import PreparedRequest

def test_digest_auth_init_and_call():
    """
    Test that calling the auth object on a request initializes thread-local state
    and registers the response hooks. 
    Uses a real PreparedRequest to ensure hooks are correctly appended to the request's hook system.
    """
    auth = HTTPDigestAuth("myuser", "mypass")
    
    # Use a real PreparedRequest to simulate actual usage
    request = PreparedRequest()
    request.prepare_method("GET")
    request.prepare_url("http://example.com", None)
    # PreparedRequest initializes hooks as {'response': []}
    
    # Apply auth
    returned_request = auth(request)
    
    assert returned_request is request
    
    # Check that hooks were registered in the 'response' list
    # The list should contain the auth handlers
    assert len(request.hooks['response']) >= 2
    
    # Verify specific handlers are present
    assert auth.handle_401 in request.hooks['response']
    assert auth.handle_redirect in request.hooks['response']
    
    # Verify thread local state initialization
    # We check these internal attributes to ensure the state machine is ready for the first 401
    assert hasattr(auth._thread_local, "init")
    assert auth._thread_local.init is True
    assert auth._thread_local.last_nonce == ""
    assert auth._thread_local.nonce_count == 0
    assert auth._thread_local.chal == {}
    assert auth._thread_local.num_401_calls == 1