## 2024-05-23 - [Telegram WebApp Authentication Bypass]
**Vulnerability:** The `authorize_webapp` function in `src/gardarika/admin.py` was trusting the `init_data` payload from the client without verifying the cryptographic signature (HMAC-SHA256).
**Learning:** Even internal admin tools must verify the integrity of data received from the client, especially when it grants privileged access. The `tg_id` can be easily spoofed if the signature is not checked.
**Prevention:** Always implement signature verification for third-party platform data (like Telegram WebApps) according to their official documentation. Never trust client-side data for authorization without validation.
