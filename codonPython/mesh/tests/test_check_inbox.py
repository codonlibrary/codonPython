import pytest

import mesh


def test_CheckInbox_ValidRequest_ReturnsJson(requests_mock, mesh_connection):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=200,
        json={"messages": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    )
    test_check_inbox_count = mesh_connection.check_inbox()
    assert requests_mock.call_count == 1
    assert test_check_inbox_count == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_CheckInbox_403StatusCode_ReturnsAuthenticationError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.check_inbox()
    assert requests_mock.call_count == 1


def test_CheckInbox_400StatusCode_ReturnsUnknownError(requests_mock, mesh_connection):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.check_inbox()
    assert requests_mock.call_count == 1
