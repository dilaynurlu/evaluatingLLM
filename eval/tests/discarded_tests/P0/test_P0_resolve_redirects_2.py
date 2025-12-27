import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the configured max_redirects limit.
    """
    session = Session()
    session.max_redirects = 2
    
    req = PreparedRequest()
    req.url = "http://example.com/loop"
    
    # A response that triggers a redirect
    resp = Response()
    resp.url = "http://example.com/loop"
    resp.raw = MagicMock()
    
    # Always return a redirect target to simulate infinite loop
    session.get_redirect_target = MagicMock(return_value="http://example.com/loop")
    
    # Return a new response object each time to simulate a chain
    def side_effect_send(*args, **kwargs):
        r = Response()
        r.url = "http://example.com/loop"
        r.raw = MagicMock()
        return r
    session.send = MagicMock(side_effect=side_effect_send)
    
    # Stub other methods
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    
    with patch("requests.sessions.extract_cookies_to_jar"):
        with pytest.raises(TooManyRedirects) as excinfo:
            list(session.resolve_redirects(resp, req))
            
    assert "Exceeded 2 redirects" in str(excinfo.value)


'''
Execution failed:

with patch("requests.sessions.extract_cookies_to_jar"):
            with pytest.raises(TooManyRedirects) as excinfo:
>               list(session.resolve_redirects(resp, req))

eval/tests/generated_tests/P0/resolve_redirects/test_P0_resolve_redirects_2.py:41: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <requests.sessions.Session object at 0xffffb372ec10>
resp = <Response [None]>, req = <PreparedRequest [None]>, stream = False
timeout = None, verify = True, cert = None, proxies = None
yield_requests = False, adapter_kwargs = {}, hist = [<Response [None]>]
url = 'http://example.com/loop', previous_fragment = ''
prepared_request = <PreparedRequest [None]>
parsed = ParseResult(scheme='http', netloc='example.com', path='/loop', params='', query='', fragment='')
purged_headers = ('Content-Length', 'Content-Type', 'Transfer-Encoding')

    def resolve_redirects(
        self,
        resp,
        req,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
        yield_requests=False,
        **adapter_kwargs,
    ):
        """Receives a Response. Returns a generator of Responses or Requests."""
    
        hist = []  # keep track of history
    
        url = self.get_redirect_target(resp)
        previous_fragment = urlparse(req.url).fragment
        while url:
            prepared_request = req.copy()
    
            # Update history and keep track of redirects.
            # resp.history must ignore the original request in this loop
            hist.append(resp)
            resp.history = hist[1:]
    
            try:
                resp.content  # Consume socket so it can be released
            except (ChunkedEncodingError, ContentDecodingError, RuntimeError):
                resp.raw.read(decode_content=False)
    
            if len(resp.history) >= self.max_redirects:
                raise TooManyRedirects(
                    f"Exceeded {self.max_redirects} redirects.", response=resp
                )
    
            # Release the connection back into the pool.
            resp.close()
    
            # Handle redirection without scheme (see: RFC 1808 Section 4)
            if url.startswith("//"):
                parsed_rurl = urlparse(resp.url)
                url = ":".join([to_native_string(parsed_rurl.scheme), url])
    
            # Normalize url case and attach previous fragment if needed (RFC 7231 7.1.2)
            parsed = urlparse(url)
            if parsed.fragment == "" and previous_fragment:
                parsed = parsed._replace(fragment=previous_fragment)
            elif parsed.fragment:
                previous_fragment = parsed.fragment
            url = parsed.geturl()
    
            # Facilitate relative 'location' headers, as allowed by RFC 7231.
            # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
            # Compliant with RFC3986, we percent encode the url.
            if not parsed.netloc:
                url = urljoin(resp.url, requote_uri(url))
            else:
                url = requote_uri(url)
    
            prepared_request.url = to_native_string(url)
    
            self.rebuild_method(prepared_request, resp)
    
            # https://github.com/psf/requests/issues/1084
            if resp.status_code not in (
                codes.temporary_redirect,
                codes.permanent_redirect,
            ):
                # https://github.com/psf/requests/issues/3490
                purged_headers = ("Content-Length", "Content-Type", "Transfer-Encoding")
                for header in purged_headers:
>                   prepared_request.headers.pop(header, None)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E                   AttributeError: 'NoneType' object has no attribute 'pop'

requests/src/requests/sessions.py:231: AttributeError
'''