import pytest

import mesh


@pytest.fixture
def base_params():
    return {
        "message_id": "1",
    }


def test_DownloadMessage_SimpleFileReturnsCorrect(
    requests_mock, mesh_connection, base_params, tmpdir
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}",
        request_headers={
            "Authorization": "xxxauthorizationxxx",
            "Accept-Encoding": "gzip",
        },
        status_code=200,
        headers={"Mex-FileName": "test.txt", "Mex-MessageType": "DATA"},
        text="test",
    )
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "content": b"test",
        "headers": {"Mex-FileName": "test.txt", "Mex-MessageType": "DATA",},
        "data": True,
    }
    p = tmpdir.mkdir("save")
    base_params["save_folder"] = str(p)
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "content": b"test",
        "headers": {"Mex-FileName": "test.txt", "Mex-MessageType": "DATA",},
        "data": True,
    }
    assert p.join("test.txt").read() == "test"


def test_DownloadMessage_ZipFileReturnsCorrect(
    requests_mock, mesh_connection, base_params, tmpdir
):
    import gzip

    message = gzip.compress(b"test")
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}",
        request_headers={
            "Authorization": "xxxauthorizationxxx",
            "Accept-Encoding": "gzip",
        },
        status_code=200,
        headers={
            "Mex-FileName": "test.txt",
            "Content-Encoding": "gzip",
            "Mex-MessageType": "DATA",
        },
        content=message,
    )
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test",
        "headers": {
            "Mex-FileName": "test.txt",
            "Content-Encoding": "gzip",
            "Mex-MessageType": "DATA",
        },
        "data": True,
    }
    p = tmpdir.mkdir("save")
    base_params["save_folder"] = str(p)
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test",
        "headers": {
            "Mex-FileName": "test.txt",
            "Content-Encoding": "gzip",
            "Mex-MessageType": "DATA",
        },
        "data": True,
    }
    assert p.join("test.txt").read() == "test"


def test_DownloadMessage_NonDeliveryReturnsCorrect(
    requests_mock, mesh_connection, base_params, tmpdir
):
    headers = {
        "Mex-FileName": "test.txt",
        "LinkedMessageId": "1",
        "Mex-MessageType": "REPORT",
    }
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}",
        request_headers={
            "Authorization": "xxxauthorizationxxx",
            "Accept-Encoding": "gzip",
        },
        status_code=200,
        headers=headers,
    )
    assert mesh_connection.download_message(**base_params) == {
        "filename": None,
        "content": None,
        "headers": headers,
        "data": False,
    }
    p = tmpdir.mkdir("save")
    base_params["save_folder"] = str(p)
    assert mesh_connection.download_message(**base_params) == {
        "filename": None,
        "content": None,
        "headers": headers,
        "data": False,
    }
    assert p.join(
        "Non delivery report: 1.txt"
    ).read() == "Message not delivered. All known details below\n" + str(headers)


def test_DownloadMessage_ChunkedFileReturnsCorrect(
    requests_mock, mesh_connection, base_params, tmpdir
):
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}",
        request_headers={
            "Authorization": "xxxauthorizationxxx",
            "Accept-Encoding": "gzip",
        },
        status_code=206,
        headers={
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
        },
        text="test-",
    )
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/2",
        status_code=206,
        headers={"Mex-Chunk-Range": "2:3"},
        text="test2-",
    )
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/3",
        status_code=200,
        headers={"Mex-Chunk-Range": "3:3"},
        text="test3",
    )
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test-test2-test3",
        "headers": {
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
        },
        "data": True,
    }
    p = tmpdir.mkdir("save")
    base_params["save_folder"] = str(p)
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test-test2-test3",
        "headers": {
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
        },
        "data": True,
    }
    assert p.join("test.txt").read() == "test-test2-test3"


def test_DownloadMessage_ChunkedZipFileReturnsCorrect(
    requests_mock, mesh_connection, base_params, tmpdir
):
    import gzip
    from math import floor

    message = gzip.compress(b"test-test2-test3")
    split = floor(len(message) / 3)
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}",
        status_code=206,
        headers={
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
            "Content-Encoding": "gzip",
        },
        content=message[:split],
    )
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/2",
        status_code=206,
        headers={"Mex-Chunk-Range": "2:3"},
        content=message[split : split * 2],
    )
    requests_mock.get(
        url=f"http://root/messageexchange/TestMailboxId/inbox/{base_params['message_id']}/3",
        status_code=200,
        headers={"Mex-Chunk-Range": "3:3"},
        content=message[split * 2 :],
    )
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test-test2-test3",
        "headers": {
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
            "Content-Encoding": "gzip",
        },
        "data": True,
    }
    p = tmpdir.mkdir("save")
    base_params["save_folder"] = str(p)
    assert mesh_connection.download_message(**base_params) == {
        "filename": "test.txt",
        "data": b"test-test2-test3",
        "headers": {
            "Mex-FileName": "test.txt",
            "Mex-MessageType": "DATA",
            "Mex-Chunk-Range": "1:3",
            "Content-Encoding": "gzip",
        },
        "data": True,
    }
    assert p.join("test.txt").read() == "test-test2-test3"


def test_DownloadMessage_403StatusCode_ReturnsAuthenticationError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox/8",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=403,
    )
    with pytest.raises(mesh.MESHAuthenticationError) as e:
        mesh_connection.download_message(message_id=8, save_folder="save_folder")
    assert requests_mock.call_count == 1


def test_DownloadMessage_404StatusCode_ReturnsMessageDoesNotExistError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox/9",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=404,
    )
    with pytest.raises(mesh.MESHMessageMissing) as e:
        mesh_connection.download_message(message_id=9, save_folder="save_folder")
    assert requests_mock.call_count == 1


def test_DownloadMessage_410StatusCode_ReturnsMessageAlreadyDownloadedError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox/10",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=410,
    )
    with pytest.raises(mesh.MESHMessageAlreadyDownloaded) as e:
        mesh_connection.download_message(message_id=10, save_folder="save_folder")
    assert requests_mock.call_count == 1


def test_DownloadMessage_400StatusCode_RaisesUnknownError(
    requests_mock, mesh_connection
):
    requests_mock.get(
        url="http://root/messageexchange/TestMailboxId/inbox/10",
        request_headers={"Authorization": "xxxauthorizationxxx"},
        status_code=400,
    )
    with pytest.raises(mesh.MESHUnknownError) as e:
        mesh_connection.download_message(message_id=10, save_folder="save_folder")
    assert requests_mock.call_count == 1
