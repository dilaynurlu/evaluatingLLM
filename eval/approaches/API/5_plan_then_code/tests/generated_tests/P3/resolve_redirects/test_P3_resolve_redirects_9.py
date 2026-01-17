import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request
from requests.exceptions import UnrewindableBodyError

def test_resolve_redirects_unrewindable_body():
    """
    Test that UnrewindableBodyError is raised if the body cannot be rewound
    (e.g., a stream that consumed content) during a redirect that preserves the body.
    """
    session = Session()
    
    # Mock a file-like body that raises OSError on tell() or seek()
    mock_body = Mock()
    mock_body.tell.return_value = 0
    mock_body.seek.side_effect = OSError("Seek failed")
    # Mark it as iterable to be treated as a stream
    mock_body.__iter__ = Mock(return_value=iter([b"data"]))
    
    # Prepare request manually to attach the mock body properly
    req = Request(method="POST", url="http://example.com/upload", data=mock_body).prepare()
    
    # Check if _body_position was set during prepare (indicates rewind attempt is possible)
    assert req._body_position == 0
    
    resp = Response()
    # 307 preserves body, so it triggers rewind attempt
    resp.status_code = 307 
    resp.headers["Location"] = "/upload_retry"
    resp.url = "http://example.com/upload"
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    
    # Expect UnrewindableBodyError when trying to rewind
    with pytest.raises(UnrewindableBodyError):
        next(gen)