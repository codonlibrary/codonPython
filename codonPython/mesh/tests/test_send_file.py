import pytest

import mesh


@pytest.fixture
def make_params(tmpdir):
    p = tmpdir.mkdir("folder").join("test.txt")
    p.write("test")
    params = {
        "dest_mailbox": "TESTMB",
        "message_location": str(p),
        "workflow_id": "TESTWF",
        "message_subject": "TESTSUB",
        "message_id": "TESTID",
        "process_id": "TESTPROC",
        "compress_message": True,
        "encrypted": True,
    }
    return params


def track_args(**kwargs):
    return kwargs


@pytest.fixture
def patch_message(mesh_connection, monkeypatch):
    monkeypatch.setattr(mesh_connection, "send_message", track_args)
    return mesh_connection


def test_SendFile_HandlesParams(patch_message, make_params):
    params = patch_message.send_file(**make_params)
    assert params == {
        "dest_mailbox": "TESTMB",
        "message": b"test",
        "filename": "test.txt",
        "workflow_id": "TESTWF",
        "message_subject": "TESTSUB",
        "message_id": "TESTID",
        "process_id": "TESTPROC",
        "compress_message": True,
        "encrypted": True,
    }
