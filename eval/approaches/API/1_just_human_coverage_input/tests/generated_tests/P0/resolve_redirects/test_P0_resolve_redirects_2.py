import pytest
from unittest.mock import Mock
from requests import Session, Request, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the redirect chain exceeds max_redirects.
    """
    session = Session()
    session.max_redirects = 1
    
    req = Request('GET', 'http://example.com/start').prepare()
    
    # First response redirects to /mid
    resp1 = Response()
    resp1.status_code = 302
    resp1.url = 'http://example.com/start'
    resp1.headers['Location'] = 'http://example.com/mid'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    
    # Second response redirects to /end
    # This response will be returned by send(), causing the loop to repeat
    resp2 = Response()
    resp2.status_code = 302
    resp2.url = 'http://example.com/mid'
    resp2.headers['Location'] = 'http://example.com/end'
    resp2._content = b""
    resp2._content_consumed = True
    
    session.send = Mock(return_value=resp2)
    
    gen = session.resolve_redirects(resp1, req)
    
    # The first iteration processes resp1, calls send(), gets resp2, and yields resp2.
    # The history after this step will contain [resp1].
    first_yield = next(gen)
    assert first_yield == resp2
    
    # The generator loop continues because resp2 is also a redirect.
    # It appends resp2 to history. History is now [resp1, resp2]. length is 2.
    # max_redirects is 1. Since 2 > 1, it should raise TooManyRedirects.
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)