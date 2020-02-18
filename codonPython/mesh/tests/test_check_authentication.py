import pytest

import mesh


def test_CheckAuthentication_ValidRequest_ReturnsTrue(requests_mock, mesh_connection):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId", status_code=200,
    )
    test_check_authentication = mesh_connection.check_authentication()
    assert requests_mock.call_count == 1
    assert test_check_authentication


def test_CheckAuthentication_HasRequiredHeaders(requests_mock, mesh_connection):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=200,
    )
    mesh_connection.check_authentication()
    assert requests_mock.call_count == 1
    assert all(
        header in requests_mock.request_history[0].headers
        for header in [
            "Mex-ClientVersion",
            "Mex-OSArchitecture",
            "Mex-OSName",
            "Mex-OSVersion",
        ]
    )


def test_CheckAuthentication_403StatusCode_ReturnsFalse(requests_mock, mesh_connection):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId", status_code=403,
    )
    test_check_authentication = mesh_connection.check_authentication()
    assert requests_mock.call_count == 1
    assert not test_check_authentication


def test_CheckAuthentication_400StatusCode_ReturnsUnknownError(
    requests_mock, mesh_connection
):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId", status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.check_authentication()
    assert requests_mock.call_count == 1
