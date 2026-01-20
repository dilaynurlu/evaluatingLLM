
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response
from unittest.mock import MagicMock

def test_HTTPDigestAuth_call_returns_request():
    auth = HTTPDigestAuth("user", "pass")
    r = MagicMock(spec=Response)
    r.body = MagicMock()
    r.headers = {}
    
    result = auth(r)
    assert result is r
