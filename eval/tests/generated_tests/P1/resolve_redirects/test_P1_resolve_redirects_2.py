import pytest
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects
from unittest.mock import Mock

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the configured max_redirects.
    """
    session = Session()
    session.max_redirects = 1  # Allow only 1 hop, fail on 2nd redirect attempt
    
    req = Request('GET', 'http://example.com/1').prepare()
    
    # First response: Redirect /1 -> /2
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = '/2'
    resp1.url = 'http://example.com/1'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.request = req
    
    # Second response: Redirect /2 -> /3 (This causes the loop to detect too many redirects)
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = '/3'
    resp2.url = 'http://example.com/2'
    resp2._content = b""
    resp2.raw = Mock()
    resp2.request = req 
    
    session.send = Mock(return_value=resp2)
    
    gen = session.resolve_redirects(resp1, req)
    
    # The generator should yield resp2 (the result of the first redirect),
    # but then when it tries to process resp2 (which is also a redirect),
    # it checks history length and raises.
    
    # Depending on implementation detail:
    # 1. Yields resp2.
    # 2. Next iteration calls next(gen).
    # 3. Detects max redirects exceeded. Raises.
    
    # We use list() to consume the generator.
    with pytest.raises(TooManyRedirects) as excinfo:
        list(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)