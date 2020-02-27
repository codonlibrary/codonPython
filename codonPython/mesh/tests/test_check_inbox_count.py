import pytest

import codonPython.mesh as mesh


def test_CheckInboxCount_ValidRequest_ReturnsJson(requests_mock, mesh_connection):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/count",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=200,
        json={"count": 100},
    )
    test_check_inbox_count = mesh_connection.check_inbox_count()
    assert test_check_inbox_count == 100
    assert requests_mock.call_count == 1


def test_CheckInboxCount_403StatusCode_ReturnsAuthenticationError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/count",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError):
        mesh_connection.check_inbox_count()
    assert requests_mock.call_count == 1


def test_CheckInboxCount_400StatusCode_RaisesUnknownError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/count",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError):
        mesh_connection.check_inbox_count()
    assert requests_mock.call_count == 1
