import base64
import pytest
from requests import Session, PreparedRequest, Response

def test_rebuild_auth_strips_old_and_applies_new_netrc_auth(tmp_path, monkeypatch):
    """
    Test the full integration scenario: 
    1. Old Auth is stripped due to cross-domain redirect.
    2. New Auth is applied from .netrc for the new domain.
    """
    # Configuration
    new_host = "new-host.com"
    username = "newuser"
    password = "newpass"
    
    # Setup .netrc for the NEW host
    netrc_content = f"machine {new_host} login {username} password {password}"
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content, encoding="utf-8")
    monkeypatch.setenv("NETRC", str(netrc_file))

    session = Session()
    session.trust_env = True

    # Request to new-host, initially carrying old-host credentials
    p_req = PreparedRequest()
    p_req.prepare(
        method="GET", 
        url=f"http://{new_host}/resource",
        headers={"Authorization": "Bearer old_secret"}
    )

    # Redirect came from old-host (different domain)
    original_req = PreparedRequest()
    original_req.url = "http://old-host.com/resource"
    response = Response()
    response.request = original_req

    # Execute
    session.rebuild_auth(p_req, response)

    # Calculate expected credentials
    credentials = f"{username}:{password}"
    b64_credentials = base64.b64encode(credentials.encode("latin1")).decode("ascii")
    expected_header = f"Basic {b64_credentials}"

    # Assert
    val = p_req.headers.get("Authorization")
    assert val is not None
    assert val != "Bearer old_secret", "Old credentials should have been stripped"
    assert val == expected_header, "New .netrc credentials should have been applied"