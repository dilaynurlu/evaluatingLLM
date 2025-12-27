import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_reusing_nonce():
    """
    Test that reusing a nonce increments the nonce_count (nc).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = MagicMock(spec=requests.PreparedRequest)
    req.method = "GET"
    req.url = "http://example.com"
    req.body = None
    req.register_hook = MagicMock()
    auth(req)
    
    # 1. First 401 with nonce="A"
    r_401_1 = MagicMock(spec=requests.Response)
    r_401_1.request = req
    req.copy.return_value = MagicMock(headers={})
    
    r_401_1.headers = {
        "www-authenticate": 'Digest realm="r", nonce="A", qop="auth"'
    }
    r_401_1.status_code = 401
    r_401_1.is_redirect = False
    r_401_1.content = b""
    r_401_1.raw = MagicMock()
    r_401_1.connection = MagicMock()
    r_401_1.connection.send.return_value = MagicMock()
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(r_401_1)
    
    # Check internal state: last_nonce should be A, count should be 1
    assert auth._thread_local.last_nonce == "A"
    assert auth._thread_local.nonce_count == 1
    
    # 2. Second 401 with SAME nonce="A"
    r_401_2 = MagicMock(spec=requests.Response)
    r_401_2.request = req
    new_req_2 = MagicMock(spec=requests.PreparedRequest)
    new_req_2.headers = {}
    new_req_2.method = "GET"
    new_req_2.url = "http://example.com"
    new_req_2._cookies = MagicMock()
    new_req_2.prepare_cookies = MagicMock()
    req.copy.return_value = new_req_2
    
    r_401_2.headers = {
        "www-authenticate": 'Digest realm="r", nonce="A", qop="auth"'
    }
    r_401_2.status_code = 401
    r_401_2.is_redirect = False
    r_401_2.content = b""
    r_401_2.raw = MagicMock()
    r_401_2.connection = MagicMock()
    r_401_2.connection.send.return_value = MagicMock()
    
    # Reset num_401_calls to allow another 401 handling
    auth._thread_local.num_401_calls = 1
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(r_401_2)
        
    # Verify nc incremented
    assert auth._thread_local.nonce_count == 2
    
    auth_header = new_req_2.headers.get("Authorization")
    assert "nc=00000002" in auth_header


'''
Execution failed:

with patch("requests.auth.extract_cookies_to_jar"):
>           auth.handle_401(r_401_1)

eval/tests/generated_tests/P1/HTTPDigestAuth/test_P1_HTTPDigestAuth_9.py:35: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
requests/src/requests/auth.py:273: in handle_401
    prep.headers["Authorization"] = self.build_digest_header(
requests/src/requests/auth.py:183: in build_digest_header
    p_parsed = urlparse(url)
               ^^^^^^^^^^^^^
/usr/local/lib/python3.11/urllib/parse.py:395: in urlparse
    splitresult = urlsplit(url, scheme, allow_fragments)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

url = <MagicMock name='mock.request.copy().url.decode().decode().lstrip().replace().replace().replace()' id='281472945026384'>
scheme = '', allow_fragments = True

    @functools.lru_cache(typed=True)
    def urlsplit(url, scheme='', allow_fragments=True):
        """Parse a URL into 5 components:
        <scheme>://<netloc>/<path>?<query>#<fragment>
    
        The result is a named 5-tuple with fields corresponding to the
        above. It is either a SplitResult or SplitResultBytes object,
        depending on the type of the url parameter.
    
        The username, password, hostname, and port sub-components of netloc
        can also be accessed as attributes of the returned object.
    
        The scheme argument provides the default value of the scheme
        component when no scheme is found in url.
    
        If allow_fragments is False, no attempt is made to separate the
        fragment component from the previous component, which can be either
        path or query.
    
        Note that % escapes are not expanded.
        """
    
        url, scheme, _coerce_result = _coerce_args(url, scheme)
        # Only lstrip url as some applications rely on preserving trailing space.
        # (https://url.spec.whatwg.org/#concept-basic-url-parser would strip both)
        url = url.lstrip(_WHATWG_C0_CONTROL_OR_SPACE)
        scheme = scheme.strip(_WHATWG_C0_CONTROL_OR_SPACE)
    
        for b in _UNSAFE_URL_BYTES_TO_REMOVE:
            url = url.replace(b, "")
            scheme = scheme.replace(b, "")
    
        allow_fragments = bool(allow_fragments)
        netloc = query = fragment = ''
        i = url.find(':')
>       if i > 0 and url[0].isascii() and url[0].isalpha():
           ^^^^^
E       TypeError: '>' not supported between instances of 'MagicMock' and 'int'

/usr/local/lib/python3.11/urllib/parse.py:504: TypeError
'''
