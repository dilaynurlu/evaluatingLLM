import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_redirect_counter_reset():
    """
    Test that handle_redirect correctly resets the num_401_calls counter.
    This ensures that if a redirect occurs during authentication, 
    the client has a fresh allowance of retries for the new location.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/source").prepare()
    auth(req)
    
    # Set counter to a high value indicating previous attempts
    auth._thread_local.num_401_calls = 5
    
    # Create a Redirect Response (302 Found)
    response = Response()
    response.status_code = 302
    response.headers["Location"] = "http://example.org/dest"
    response.url = "http://example.org/source"
    response.request = req
    
    # Ensure properties needed for is_redirect are met
    # Response.is_redirect checks 'location' in headers and status code in REDIRECT_STATI
    
    # Call the hook
    auth.handle_redirect(response)
    
    # Assert counter is reset to 1
    assert auth._thread_local.num_401_calls == 1