import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_uri_query_params():
    """
    Test that the 'uri' directive in the Authorization header correctly includes 
    path and query parameters.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # URL with path and query parameters
    url = "http://example.com/api/v1/resource?foo=bar&baz=1"
    req = requests.Request("GET", url).prepare()
    
    resp = requests.Response()
    resp.status_code = 401
    resp.url = url
    resp.request = req
    resp.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n", qop="auth"'
    }
    resp._content = b""
    
    resp.connection = Mock()
    resp.raw = Mock()
    resp.connection.send.return_value = requests.Response()
    
    auth(req)
    auth.handle_401(resp)
    
    sent_req = resp.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    # The URI field should be exactly the path + query
    expected_uri = "/api/v1/resource?foo=bar&baz=1"
    assert f'uri="{expected_uri}"' in auth_header