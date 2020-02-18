import pytest


def mock_generate_authorization(*args):
    return "xxxauthorizationxxx"


@pytest.fixture
def mesh_connection(monkeypatch):
    import mesh

    monkeypatch.setattr(
        mesh.mesh, "generate_authorization", mock_generate_authorization
    )

    return mesh.MESHConnection(
        mailbox="TestMailboxId",
        password="secret_password",
        api_shared_key="api_shared_key",
        cert_loc="keys/mesh.cert",
        key_loc="keys/mesh.key",
        base_ca_loc="keys/mesh.ca-bundle",
        root_url="http://root",
    )
