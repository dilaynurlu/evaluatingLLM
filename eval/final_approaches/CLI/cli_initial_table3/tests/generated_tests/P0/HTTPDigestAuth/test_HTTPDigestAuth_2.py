from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_2():
    auth = HTTPDigestAuth("user", "pass")
    request = Mock()
    request.headers = {}
    request.register_hook = Mock()
    request.body = None
    
    auth(request)
    
    assert request.register_hook.call_count == 2
    # Verify calls to register_hook
    calls = request.register_hook.call_args_list
    # The order of hooks might vary but usually it's consistent.
    # Let's check if both hooks are registered.
    registered_hooks = [call[0][1].__name__ for call in calls]
    assert "handle_401" in registered_hooks
    assert "handle_redirect" in registered_hooks
