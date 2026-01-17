import pytest
from unittest.mock import Mock
import requests
from requests.auth import HTTPDigestAuth

def test_http_digest_auth_retry_limit():
    """
    Test that HTTPDigestAuth prevents infinite loops by limiting the number of 401 retries.
    Simulates a server persistently returning 401.
    """
    url = "http://example.org/loop"
    auth = HTTPDigestAuth("user", "pass")
    
    req = requests.Request("GET", url).prepare()
    
    # Response setup
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.url = url
    resp_401.status_code = 401
    resp_401.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    resp_401._content = b""
    resp_401.raw = Mock()
    
    mock_connection = Mock()
    resp_401.connection = mock_connection
    
    # Configure mock to always return 401
    # Note: requests.adapters.HTTPAdapter usually creates new Response objects.
    # We return the *same* response object for simplicity, or a sequence.
    # The logic relies on calling handle_401 recursively or sequentially?
    # Actually, handle_401 calls connection.send(), which returns a response.
    # If that response is 401, the requests dispatch loop would call handle_401 again.
    # However, inside `handle_401`, it captures the response from `send`.
    # It then returns that response. It does *not* recursively call itself usually;
    # it relies on the caller (requests.Session.send) to call hooks again? 
    # WAIT: requests `Session` loop handles redirects. Auth challenge is handled inside `handle_401`.
    # `handle_401` performs the retry *internally* and returns the result.
    # If the result of the retry is *also* 401, `handle_401` returns it.
    # The *outer* requests loop might see 401 and call hook again?
    # `HTTPDigestAuth` implements a counter in `handle_401`.
    # If we are in `handle_401`, we are already processing a 401.
    # If we retry and get 401, we return it.
    # If the outer loop calls us again with that new 401, we need to know we've already tried.
    
    # Simulation:
    # 1. First 401 received. handle_401 called.
    # 2. It sends a request. Mock returns 401.
    # 3. handle_401 returns that 401.
    # 4. In a real scenario, requests might invoke hooks again on this new response.
    # We manually simulate this sequence to verify the counter logic prevents a second retry.
    
    mock_connection.send = Mock(return_value=resp_401)
    
    # Init
    auth(req)
    
    # First 401 handling
    result1 = auth.handle_401(resp_401)
    
    # Assertions for first pass
    assert result1.status_code == 401
    assert mock_connection.send.call_count == 1
    
    # Now simulate the outer loop calling handle_401 again on the new response (result1)
    # The counter should now prevent a new request
    result2 = auth.handle_401(result1)
    
    # Assertions for second pass
    # Should be the same response, no new send call
    assert result2 is result1
    assert mock_connection.send.call_count == 1 # Still 1, didn't increment