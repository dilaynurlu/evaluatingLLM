import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_handle_non_401_response():
    """
    Test that a non-401 response is passed through untouched.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    response = Mock()
    response.status_code = 200
    
    # Act
    result = auth.handle_401(response)
    
    # Assert
    assert result is response