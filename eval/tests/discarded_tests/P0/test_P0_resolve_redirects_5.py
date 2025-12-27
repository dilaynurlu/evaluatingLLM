import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_yield_requests_true():
    """
    Test the behavior when yield_requests=True.
    The generator should yield PreparedRequest objects and NOT call session.send().
    """
    session = Session()
    # Set max_redirects to 1 to prevent potential infinite loops in test
    # since yield_requests doesn't update response/url automatically in the loop logic 
    # in the same way (it bypasses send).
    session.max_redirects = 1
    
    req = PreparedRequest()
    req.url = "http://example.com/source"
    
    resp = Response()
    resp.url = "http://example.com/source"
    resp.raw = MagicMock()
    
    # We need get_redirect_target to return a URL to enter the loop
    session.get_redirect_target = MagicMock(return_value="http://example.com/next")
    
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    
    # We must mock extract_cookies_to_jar to avoid errors
    with patch("requests.sessions.extract_cookies_to_jar"):
        gen = session.resolve_redirects(resp, req, yield_requests=True)
        item = next(gen)
        
    # Assert that we got a request, not a response
    assert isinstance(item, PreparedRequest)
    assert item.url == "http://example.com/next"
    
    # Ensure send was NOT called
    session.send.assert_not_called()

'''
Execution failed:

# We must mock extract_cookies_to_jar to avoid errors
        with patch("requests.sessions.extract_cookies_to_jar"):
            gen = session.resolve_redirects(resp, req, yield_requests=True)
>           item = next(gen)
                   ^^^^^^^^^

eval/tests/generated_tests/P0/resolve_redirects/test_P0_resolve_redirects_5.py:34: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <requests.sessions.Session object at 0xffffb2a3c110>
resp = <Response [None]>, req = <PreparedRequest [None]>, stream = False
timeout = None, verify = True, cert = None, proxies = None
yield_requests = True, adapter_kwargs = {}, hist = [<Response [None]>]
url = 'http://example.com/next', previous_fragment = ''
prepared_request = <PreparedRequest [None]>
parsed = ParseResult(scheme='http', netloc='example.com', path='/next', params='', query='', fragment='')
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