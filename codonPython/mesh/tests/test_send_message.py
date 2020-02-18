import pytest
import mesh


@pytest.fixture
def base_params():
    return {
        "dest_mailbox": "TESTMB",
        "message": b"TEST",
        "filename": "TEST.txt",
        "workflow_id": "TESTWF",
    }


@pytest.fixture
def base_headers():
    return {
        "Authorization": "xxxauthorizationxxx",
        "Content-Type": "application/octet-stream",
        "Mex-From": "TestMailboxId",
        "Mex-To": "TESTMB",
        "Mex-WorkflowId": "TESTWF",
        "Mex-FileName": "TEST.txt",
        "Mex-MessageType": "DATA",
        "Mex-Version": "1.0",
    }


def test_SendMessage_403_RaisesAuthenticationError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1


def test_SendMessage_417_RaisesRecipientError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=417,
    )
    with pytest.raises(mesh.MESHInvalidRecipient) as e:
        mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1


def test_SendMessage_400_RaisesUnknownError(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1


def test_SendMessage_ValidHash(
    mesh_connection, requests_mock, base_params, base_headers
):
    import hashlib

    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    checksum = hashlib.md5(base_params["message"]).hexdigest()
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].headers["Mex-Checksum"] == f"md5 {checksum}"


def test_SendMessage_AbsentOptional_Skipped(
    mesh_connection, requests_mock, base_params, base_headers
):
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert not any(
        header in requests_mock.request_history[0].headers
        for header in [
            "Mex-ProcessID",
            "Mex-LocalID",
            "Mex-Subject",
            "Mex-Content-Encrypted",
        ]
    )


def test_SendMessage_PresentSubject_Included(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["message_subject"] = "TESTSUB"
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].headers["Mex-Subject"] == "TESTSUB"


def test_SendMessage_PresentMessageID_Included(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["message_id"] = "TESTMSG"
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].headers["Mex-LocalID"] == "TESTMSG"


def test_SendMessage_PresentProcess_Included(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["process_id"] = "TESTPROC"
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].headers["Mex-ProcessID"] == "TESTPROC"


def test_SendMessage_Encrypted_Included(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["encrypted"] = True
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert "Mex-Content-Encrypted" in requests_mock.request_history[0].headers


def test_compress_if_set(mesh_connection, requests_mock, base_params, base_headers):
    import gzip

    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    expected_message = gzip.compress(base_params["message"])
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert "Mex-Content-Compressed" in requests_mock.request_history[0].headers
    assert requests_mock.request_history[0].headers["Content-Encoding"] == "gzip"
    assert requests_mock.request_history[0].body == expected_message


def test_no_compress_if_not_set(
    mesh_connection, requests_mock, base_params, base_headers
):
    base_params["compress_message"] = False
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert "Mex-Content-Compressed" not in requests_mock.request_history[0].headers
    assert "Content-Encoding" not in requests_mock.request_history[0].headers
    assert requests_mock.request_history[0].body == base_params["message"]


class Tracker:
    def __init__(self):
        self.count = 0
        self.data = []

    def inc(self, **kwargs):
        self.count += 1
        self.data.append(kwargs)


def test_chunk_massive_file(
    mesh_connection, requests_mock, base_params, base_headers, monkeypatch
):
    chunks_sent = Tracker()
    monkeypatch.setattr(mesh_connection, "send_message_chunk", chunks_sent.inc)
    base_params["compress_message"] = False
    base_params["message"] = ("x" * 200000000).encode()
    requests_mock.post(
        url="http://root/messageexchange/TestMailboxId/outbox",
        request_headers=base_headers,
        status_code=202,
        json={"messageID": "1"},
    )
    mesh_connection.send_message(**base_params)
    assert requests_mock.call_count == 1
    assert requests_mock.request_history[0].headers["Mex-Chunk-Range"] == "1:3"
    assert requests_mock.request_history[0].body == base_params["message"][0:80000000]
    assert chunks_sent.count == 2
    assert (
        chunks_sent.data[0]["message_chunk"]
        == base_params["message"][80000000:160000000]
    )
    assert (
        chunks_sent.data[1]["message_chunk"]
        == base_params["message"][160000000:240000000]
    )
    assert chunks_sent.data[0]["message_id"] == "1"
    assert chunks_sent.data[1]["message_id"] == "1"
    assert chunks_sent.data[0]["chunk_no"] == 2
    assert chunks_sent.data[1]["chunk_no"] == 3
