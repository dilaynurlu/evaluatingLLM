import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_relative_url_and_fragment_inheritance():
    """
    Test handling of relative URLs in Location header and fragment inheritance.
    If the redirect URL has no fragment, it should inherit the fragment from the original request.
    Also validates strict handling of relative paths (urljoin).
    """
    session = Session()
    session.send = Mock()

    # Original URL has a fragment
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/documents/v1/index.html?view=full#section-5')

    # Redirect is relative and has NO fragment
    resp = Response()
    resp.status_code = 302
    # The 'url' attribute of response is the effective URL of the response
    resp.url = 'http://example.com/documents/v1/index.html' 
    resp.headers['Location'] = '../../v2/login'
    resp.request = req
    resp._content = b""
    resp._content_consumed = True

    # Final response
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = 'http://example.com/v2/login'
    final_resp._content = b"ok"
    final_resp._content_consumed = True
    session.send.return_value = final_resp

    list(session.resolve_redirects(resp, req))

    assert session.send.call_count == 1
    sent_req = session.send.call_args[0][0]

    # Logic verification:
    # Base: http://example.com/documents/v1/index.html
    # Relative: ../../v2/login
    # 'index.html' is file, so base dir is /documents/v1/
    # .. -> /documents/
    # .. -> /
    # + v2/login -> /v2/login
    # Fragment #section-5 should be inherited because Location has none.
    
    expected_url = 'http://example.com/v2/login?view=full#section-5'
    # Wait, query params are part of the original URL string, but urljoin replaces the whole file part?
    # No, urljoin replaces the path. 
    # If the redirect is just a path, query params from original are NOT inherited automatically by RFC standards 
    # unless implemented specifically.
    # Requests implementation:
    # url = urljoin(resp.url, requote_uri(url))
    # urljoin does NOT preserve query params from the base if the relative part replaces the path/query.
    # However, fragment IS explicitly preserved by resolve_redirects logic:
    # "if parsed.fragment == "" and previous_fragment: parsed = parsed._replace(fragment=previous_fragment)"
    
    # Correct expectation: Query params from original are lost (because new URL doesn't have them), 
    # but fragment is kept.
    
    expected_url = 'http://example.com/v2/login#section-5'
    
    assert sent_req.url == expected_url