import base64
import pytest
from requests import Session, PreparedRequest, Response

def test_rebuild_auth_applies_netrc_credentials_when_trusted(tmp_path, monkeypatch):
    """
    Test that rebuild_auth applies credentials from a .netrc file 
    when trust_env is True. Verifies correct Base64 encoding dynamically.
    """
    # Configuration
    host = "example.com"
    username = "myuser"
    password = "mypass"
    
    # Create a temporary .netrc file
    netrc_content = f"machine {host} login {username} password {password}"
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content, encoding="utf-8")

    # Point NETRC environment variable to the temp file
    monkeypatch.setenv("NETRC", str(netrc_file))

    session = Session()
    session.trust_env = True

    # Prepare request for the host defined in .netrc
    p_req = PreparedRequest()
    p_req.prepare(method="GET", url=f"http://{host}/resource")

    # Response from a different origin to trigger potential auth lookups
    original_req = PreparedRequest()
    original_req.url = "http://origin.com"
    response = Response()
    response.request = original_req

    # Execute
    session.rebuild_auth(p_req, response)

    # Calculate expected Basic Auth header dynamically
    # format: "username:password" -> base64
    credentials = f"{username}:{password}"
    b64_credentials = base64.b64encode(credentials.encode("latin1")).decode("ascii")
    expected_header = f"Basic {b64_credentials}"

    # Assert
    assert "Authorization" in p_req.headers
    assert p_req.headers["Authorization"] == expected_header