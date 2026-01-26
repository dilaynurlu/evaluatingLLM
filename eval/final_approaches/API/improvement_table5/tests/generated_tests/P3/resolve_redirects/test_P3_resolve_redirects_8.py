import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import ChunkedEncodingError
from unittest.mock import MagicMock, PropertyMock

def test_resolve_redirects_content_consumption_error_recovery():
    """
    Test that if accessing resp.content raises a ChunkedEncodingError,
    the function catches it, attempts to read raw content to clear the socket,
    and closes the response.
    """
    session = Session()
    
    req = Request("GET", "http://example.com/broken").prepare()
    
    # Create a response where accessing .content raises ChunkedEncodingError
    resp = MagicMock(spec=Response)
    resp.request = req
    resp.url = "http://example.com/broken"
    resp.status_code = 302
    resp.headers = requests.structures.CaseInsensitiveDict({"Location": "/fixed"})
    resp.history = []
    
    # Mock content property to raise
    type(resp).content = PropertyMock(side_effect=ChunkedEncodingError("Connection broken"))
    
    # Mock raw object
    resp.raw = MagicMock()
    
    # Mock close method
    resp.close = MagicMock()
    
    # Mock send so loop can proceed
    session.send = MagicMock(return_value=Response())
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    
    # Trigger the logic by advancing generator
    # It will try to consume content, fail, catch exception, read raw, and continue to redirect
    next(gen)
        
    # Verify recovery logic
    resp.raw.read.assert_called_with(decode_content=False)
    resp.close.assert_called()
    
    # Verify redirection proceeded
    session.send.assert_called()