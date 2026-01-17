import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response
from requests.exceptions import TooManyRedirects
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_too_many_redirects():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session.max_redirects limit.
    """
    session = Session()
    session.max_redirects = 1
    
    req = Request('GET', 'http://example.com/1').prepare()
    
    # Resp 1 (initial)
    resp1 = Response()
    resp1.status_code = 302
    resp1.url = 'http://example.com/1'
    resp1.headers = CaseInsensitiveDict({'Location': 'http://example.com/2'})
    resp1.raw = MagicMock()
    
    # Resp 2 (returned by send, also redirects)
    resp2 = Response()
    resp2.status_code = 302
    resp2.url = 'http://example.com/2'
    resp2.headers = CaseInsensitiveDict({'Location': 'http://example.com/3'})
    resp2.raw = MagicMock()
    
    session.send = Mock(return_value=resp2)
    
    gen = session.resolve_redirects(resp1, req)
    
    # First iteration yields resp2 (1st redirect successful)
    r = next(gen)
    assert r.url == 'http://example.com/2'
    
    # Second iteration should fail because max_redirects=1 and we are attempting a 2nd jump
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)