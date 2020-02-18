import pytest
import mesh


@pytest.fixture
def base_params():
    return {
        "message_id": "1",
        "message_chunk": b"TEST",
        "chunk_no": 2,
        "chunk_range": 3,
    }


@pytest.fixture
def base_headers():
    return {
        "Authorization": "xxxauthorizationxxx",
        "Content-Type": "application/octet-stream",
        "Mex-From": "TestMailboxId",
        "Mex-Chunk-Range": "2:3",
    }


def test_SendMessageChunk_403_RaisesAuthenticationError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url=f"http://root/messageexchange/TestMailboxId/outbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.send_message_chunk(**base_params)


def test_SendMessageChunk_400_RaisesUnknownError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url=f"http://root/messageexchange/TestMailboxId/outbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.send_message_chunk(**base_params)


def test_SendMessageChunk_Valid_SentOnce(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url=f"http://root/messageexchange/TestMailboxId/outbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=202,
    )
    mesh_connection.send_message_chunk(**base_params)
    assert requests_mock.call_count == 1


def test_SendMessageChunk_Compressed_CorrectHeaders(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url=f"http://root/messageexchange/TestMailboxId/outbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=202,
    )
    mesh_connection.send_message_chunk(**base_params)
    assert requests_mock.request_history[0].headers["Content-Encoding"] == "gzip"


def test_SendMessageChunk_NotCompressed_CorrectHeaders(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["compressed"] = False
    requests_mock.post(
        url=f"http://root/messageexchange/TestMailboxId/outbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=202,
    )
    mesh_connection.send_message_chunk(**base_params)
    assert "Content-Encoding" not in requests_mock.request_history[0].headers
