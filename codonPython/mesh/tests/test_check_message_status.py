import pytest
import mesh


@pytest.fixture
def base_params():
    return {
        "message_id": "1",
    }


@pytest.fixture
def base_headers():
    return {
        "Authorization": "xxxauthorizationxxx",
    }


def test_CheckMessage_403_RaisesAuthenticationError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.check_message_status(**base_params)


def test_CheckMessage_404_RaisesMissingError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=404,
    )
    with pytest.raises(mesh.MESHMessageMissing) as e:
        mesh_connection.check_message_status(**base_params)


def test_CheckMessage_400_RaisesUnknownError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.check_message_status(**base_params)


def test_CheckMessage_300_RaisesMultipleError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=300,
    )
    with pytest.raises(mesh.MESHMultipleMatches) as e:
        mesh_connection.check_message_status(**base_params)


# Due to errors in the API, test for a 300 error sent with code 200
def test_CheckMessage_Fake300_RaisesMultipleError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=200,
        text="<html><title>300: Multiple Choices</title><body>300: Multiple Choices</body></html>",
    )
    with pytest.raises(mesh.MESHMultipleMatches) as e:
        mesh_connection.check_message_status(**base_params)


def test_CheckMessage_Valid_RequestsOnce(
    mesh_connection, requests_mock, base_params, base_headers
):
    resp = {"test": "true"}
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=200,
        json=resp,
    )
    mesh_connection.check_message_status(**base_params)
    assert requests_mock.call_count == 1


def test_CheckMessage_Valid_ReturnsJSON(
    mesh_connection, requests_mock, base_params, base_headers
):
    resp = {"test": "true"}
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/outbox/tracking/{base_params['message_id']}",
        request_headers=base_headers,
        status_code=200,
        json=resp,
    )
    assert mesh_connection.check_message_status(**base_params) == resp
