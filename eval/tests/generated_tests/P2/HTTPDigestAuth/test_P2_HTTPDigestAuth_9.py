from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_handle_redirect_resets_counter():
    # Scenario: Redirects should reset the 401 counter to allow auth on new location
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/source")
    
    # Simulate a state where we have already tried once
    auth(request)
    auth._thread_local.num_401_calls = 2
    
    # Create a redirect response
    response = Response()
    response.status_code = 302
    response.headers["location"] = "http://example.com/dest"
    
    # Call handle_redirect
    auth.handle_redirect(response)
    
    # Counter should be reset to 1
    assert auth._thread_local.num_401_calls == 1