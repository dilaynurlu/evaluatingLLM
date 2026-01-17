import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_absolute_url_preserves_fragment():
    """
    Test redirect where Location header is an absolute URL without a fragment.
    Critique addressed: Fragment Handling on Absolute URLs.
    Should preserve the fragment from the original URL.
    """
    session = Session()
    
    target_resp = Response()
    target_resp.status_code = 200
    target_resp._content = b"OK"
    target_resp._content_consumed = True
    target_resp.url = "http://example.com/new_location"
    target_resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=target_resp)
    
    # Request with fragment
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://example.com/source#original_frag"
    )
    
    # Redirect with ABSOLUTE location and NO fragment
    resp = Response()
    resp.status_code = 302
    resp.headers = CaseInsensitiveDict({"Location": "http://example.com/new_location"}) 
    resp.url = "http://example.com/source"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    resp.request = req
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    # Verify URL resolution
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # The fragment should be appended to the absolute new location
    assert sent_req.url == "http://example.com/new_location#original_frag"