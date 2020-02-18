import pytest

import mesh


def test_Ack_ValidRequest_CallsOnce(requests_mock, mesh_connection):
    requests_mock.put(
        url="http://root/messageexchange/TestMailboxId/inbox/1/status/acknowledged",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=200,
    )
    mesh_connection.ack_download_message("1")
    assert requests_mock.call_count == 1


def test_Ack_403_RaisesAuthError(requests_mock, mesh_connection):
    requests_mock.put(
        url="http://root/messageexchange/TestMailboxId/inbox/1/status/acknowledged",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.ack_download_message("1")


def test_Ack_400_RaisesUnknownError(requests_mock, mesh_connection):
    requests_mock.put(
        url="http://root/messageexchange/TestMailboxId/inbox/1/status/acknowledged",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.ack_download_message("1")
