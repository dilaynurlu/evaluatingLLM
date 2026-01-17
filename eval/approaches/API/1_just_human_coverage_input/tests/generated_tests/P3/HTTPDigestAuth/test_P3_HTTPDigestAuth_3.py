import pytest
import io
from unittest.mock import Mock
import requests
from requests.auth import HTTPDigestAuth

def test_http_digest_auth_body_rewind():
    """
    Test that the request body is rewound (seek to start position) before retrying
    with Authorization header. This ensures the full body is sent on retry.
    """
    url = "http://example.org/post"
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a request with a file-like body
    body_content = b"some data to post"
    body = io.BytesIO(body_content)
    
    req = requests.Request("POST", url, data=body).prepare()
    
    # Register hooks
    auth(req)
    
    # Simulate partial read of body during first transmission
    body.read(10)
    assert body.tell() == 10
    
    # Prepare 401 response
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.url = url
    resp_401.status_code = 401
    resp_401.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    resp_401._content = b""
    resp_401.raw = Mock()
    
    # Mock connection for retry
    mock_connection = Mock()
    resp_success = requests.Response()
    resp_success.status_code = 200
    mock_connection.send = Mock(return_value=resp_success)
    resp_401.connection = mock_connection
    
    # Wrap the body seek method to verify it's called
    # We use a side_effect to ensure the seek actually happens on the object
    original_seek = body.seek
    seek_mock = Mock(side_effect=original_seek)
    body.seek = seek_mock
    
    # Trigger handle_401
    auth.handle_401(resp_401)
    
    # Assert that seek(0) was called to reset the body for the retry
    seek_mock.assert_called_with(0)
    # Ensure position is back at start (though requests might read it again inside send,
    # the important part is it was reset before send).
    # Since we mocked send (and didn't read in mock), it should be at 0 or whatever seek set.
    assert body.tell() == 0