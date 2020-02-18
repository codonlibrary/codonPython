import pytest
import mesh


@pytest.fixture
def base_params():
    return {
        "message_id": "1",
        "chunk_no": 2,
    }


@pytest.fixture
def base_headers():
    return {"Authorization": "xxxauthorizationxxx", "Accept-Encoding": "gzip"}


def test_DownloadMessageChunk_403_RaisesAuthenticationError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.download_message_chunk(**base_params)


def test_DownloadMessageChunk_404_RaisesMissingError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=404,
    )
    with pytest.raises(mesh.MESHMessageMissing) as e:
        mesh_connection.download_message_chunk(**base_params)


def test_DownloadMessageChunk_410_RaisesGoneError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=410,
    )
    with pytest.raises(mesh.MESHMessageAlreadyDownloaded) as e:
        mesh_connection.download_message_chunk(**base_params)


def test_DownloadMessageChunk_400_RaisesUnknownError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.download_message_chunk(**base_params)


def test_DownloadMessageChunk_Valid_SentOnce(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=200,
        text="test",
    )
    mesh_connection.download_message_chunk(**base_params)
    assert requests_mock.call_count == 1


def test_DownloadMessageChunk_206_NoRaise(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=206,
        text="test",
    )
    mesh_connection.download_message_chunk(**base_params)
    assert requests_mock.call_count == 1


def test_DownloadMessageChunk_ReturnsCorrect(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/{base_params['chunk_no']}",
        request_headers=base_headers,
        status_code=200,
        text="test",
    )
    assert mesh_connection.download_message_chunk(**base_params) == b"test"
