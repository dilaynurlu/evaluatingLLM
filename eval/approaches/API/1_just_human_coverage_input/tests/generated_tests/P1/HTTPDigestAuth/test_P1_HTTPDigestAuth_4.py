import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_query_params_in_uri():
    """
    Test that query parameters in the URL are correctly included in the 'uri' directive 
    of the Digest Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # URL with query parameters
    url = "http://example.org/search?q=foo&sort=asc"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    resp = Response()
    resp.status_code = 401
    resp.headers["www-authenticate"] = 'Digest realm="search", nonce="searchnonce", qop="auth"'
    resp.request = req
    resp._content = b""
    
    mock_connection = Mock()
    mock_connection.send.return_value = Response()
    resp.connection = mock_connection
    
    auth(req)
    auth.handle_401(resp)
    
    retry_req = mock_connection.send.call_args[0][0]
    auth_header = retry_req.headers["Authorization"]
    
    # The 'uri' field must contain path and query
    # uri="/search?q=foo&sort=asc"
    
    expected_uri = '/search?q=foo&sort=asc'
    assert f'uri="{expected_uri}"' in auth_header