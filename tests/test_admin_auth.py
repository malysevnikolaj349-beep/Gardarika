import hmac
import hashlib
import os
import unittest
from unittest.mock import patch
from gardarika.admin import authorize_webapp, AdminUser

class TestWebAppAuth(unittest.TestCase):
    def setUp(self):
        self.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        self.admin_users = {
            123456789: AdminUser(tg_id=123456789, role_id="admin", is_active=True)
        }

    def _generate_hash(self, data_dict, token):
        # 1. Sort alphabetically by keys
        # 2. Format key=value
        # 3. Join with \n
        data_check_arr = []
        for key in sorted(data_dict.keys()):
            if key != 'hash':
                data_check_arr.append(f"{key}={data_dict[key]}")
        data_check_string = "\n".join(data_check_arr)

        # Secret key
        secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()

        # HMAC-SHA256
        return hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    def _get_valid_init_data(self):
        user_json = '{"id":123456789,"first_name":"Test","last_name":"User","username":"testuser","language_code":"en"}'
        init_data = {
            "query_id": "AAGL...",
            "user": user_json,
            "auth_date": "1675283456",
        }
        signature = self._generate_hash(init_data, self.token)
        init_data["hash"] = signature
        return init_data

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"})
    def test_auth_success(self):
        init_data = self._get_valid_init_data()
        admin = authorize_webapp(init_data, self.admin_users)
        self.assertEqual(admin.tg_id, 123456789)

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"})
    def test_auth_invalid_hash(self):
        init_data = self._get_valid_init_data()
        init_data['hash'] = 'invalid_hash'

        with self.assertRaises(PermissionError) as cm:
            authorize_webapp(init_data, self.admin_users)
        self.assertIn("signature mismatch", str(cm.exception))

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"})
    def test_auth_missing_hash(self):
        init_data = self._get_valid_init_data()
        del init_data['hash']

        with self.assertRaises(PermissionError) as cm:
            authorize_webapp(init_data, self.admin_users)
        self.assertIn("hash missing", str(cm.exception))

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"})
    def test_auth_fallback_tg_id(self):
        """Test fallback to 'tg_id' field if 'user' field is missing, but signature is still valid."""
        init_data = {
            "query_id": "AAGL...",
            "tg_id": "123456789", # Custom field
            "auth_date": "1675283456",
        }
        signature = self._generate_hash(init_data, self.token)
        init_data["hash"] = signature

        admin = authorize_webapp(init_data, self.admin_users)
        self.assertEqual(admin.tg_id, 123456789)

    def test_auth_missing_token(self):
        """Test that missing TELEGRAM_TOKEN raises EnvironmentError."""
        # Ensure TELEGRAM_TOKEN is not in env
        with patch.dict(os.environ, {}, clear=True):
            init_data = self._get_valid_init_data()
            with self.assertRaises(EnvironmentError) as cm:
                authorize_webapp(init_data, self.admin_users)
            self.assertIn("TELEGRAM_TOKEN", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
