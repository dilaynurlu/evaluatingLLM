
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response
from unittest.mock import MagicMock

def test_HTTPDigestAuth_handle_redirect_register():
    auth = HTTPDigestAuth("user", "pass")
    r = MagicMock(spec=Response)
    r.body = MagicMock()
    r.headers = {}
    r.method = "GET"
    r.url = "http://example.com"
    r.register_hook = MagicMock()
    
    auth(r)
    
    # Check that handle_redirect was registered
    calls = r.register_hook.call_args_list
    assert any(call[0][0] == 'response' and call[0][1] == auth.handle_redirect for call in calls)
