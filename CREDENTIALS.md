# Demo login credentials (multi-user)

Use these usernames and passwords to log in to MoneyCortex. Each user has their own accounts and data.

| Username | Password   |
|----------|------------|
| **alice**  | `alice123`  |
| **bob**    | `bob456`    |
| **priya**  | `priya789`  |
| **admin**  | `admin@2026` |

- Log in with any row above. Usernames are case-insensitive (e.g. `Alice` or `alice`).
- Each user gets a separate set of accounts and balance; data is not shared between users.
- For production, replace the in-memory `USERS` dict in `main.py` with proper authentication and hashed passwords.
