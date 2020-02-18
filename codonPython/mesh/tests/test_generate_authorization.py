import pytest
import re

import mesh


class Test_generate_authorization:
    def test_generate_authorization(self):
        nonce = "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        time = "[0-9]{12}"
        hash_out = "[0-9a-z]{64}"
        mailbox = "Test_Mailbox"
        password = "Secret_Password"
        api_shared_key = "api_shared_key"
        test_generate_authorization = mesh.generate_authorization(
            mailbox, password, api_shared_key
        )
        assert re.match(
            "NHSMESH Test_Mailbox:[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:1:[0-9]{12}:[0-9a-z]{64}",
            test_generate_authorization,
        )

    def test_generate_authorization_with_blank_mailbox(self):
        mailbox = ""
        password = "Secret_Password"
        api_shared_key = "api_shared_key"
        test_generate_authorization = mesh.generate_authorization(
            mailbox, password, api_shared_key
        )
        assert re.match(
            "NHSMESH :[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:1:[0-9]{12}:[0-9a-z]{64}",
            test_generate_authorization,
        )

    def test_generate_authorization_with_blank_password(self):
        mailbox = "Test_Mailbox"
        password = ""
        api_shared_key = "api_shared_key"
        test_generate_authorization = mesh.generate_authorization(
            mailbox, password, api_shared_key
        )
        assert re.match(
            "NHSMESH Test_Mailbox:[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:1:[0-9]{12}:[0-9a-z]{64}",
            test_generate_authorization,
        )

    def test_generate_authorization_with_blank_api_key(self):
        mailbox = "Test_Mailbox"
        password = "Secret_Password"
        api_shared_key = ""
        test_generate_authorization = mesh.generate_authorization(
            mailbox, password, api_shared_key
        )
        assert re.match(
            "NHSMESH Test_Mailbox:[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:1:[0-9]{12}:[0-9a-z]{64}",
            test_generate_authorization,
        )
