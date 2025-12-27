import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_handle_redirect_resets_counter():
    """
    Test that handle_redirect resets the num_401_calls counter.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Manually init state as we access _thread_local directly
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 5
    
    response = Mock()
    response.is_redirect = True
    
    # Act
    auth.handle_redirect(response)
    
    # Assert
    assert auth._thread_local.num_401_calls == 1