import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from database.db import get_db_connection

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def link_google_account(account_id):
    """
    Simulates linking a Google account via OAuth2 and storing the refresh token.
    In a real headless CLI, we'd use InstalledAppFlow or output a URL for the user to visit.
    """
    creds = None
    token_path = f'token_{account_id}.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"Refreshing token for {account_id}")
            creds.refresh(Request())
        else:
            print(f"To link Google account {account_id}, following the OAuth flow...")
            if os.path.exists('client_secret.json'):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    print(f"Real OAuth token saved to {token_path}")
                except Exception as e:
                    print(f"OAuth flow failed: {e}")
            else:
                print("Notice: 'client_secret.json' not found. Falling back to dummy token flow for testing.")
                creds_data = {
                    "token": "dummy_token",
                    "refresh_token": "dummy_refresh_token",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "client_id": "dummy_client_id",
                    "client_secret": "dummy_client_secret",
                    "scopes": SCOPES
                }
                with open(token_path, 'w') as token:
                    token.write(json.dumps(creds_data))
                print(f"Dummy token saved to {token_path}")

    # Store in database (Channel name updated by main.py if provided)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        refresh_token_to_store = creds.refresh_token if creds and hasattr(creds, 'refresh_token') else 'dummy_refresh_token'
        # Do not overwrite channel_name if it exists, let CLI handle it
        cursor.execute('''
            INSERT INTO accounts (platform, account_id, refresh_token)
            VALUES (?, ?, ?)
            ON CONFLICT(account_id) DO UPDATE SET
                refresh_token=excluded.refresh_token
        ''', ('youtube', account_id, refresh_token_to_store))
        conn.commit()

    print(f"Successfully linked account: {account_id}")
    return creds

def get_google_credentials(account_id):
    """
    Retrieves stored Google credentials for an account.
    """
    token_path = f'token_{account_id}.json'
    if not os.path.exists(token_path):
        return None

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Auto-refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            print(f"[Auth] Refreshing expired token for {account_id}...")
            creds.refresh(Request())
            with open(token_path, 'w') as f:
                f.write(creds.to_json())
            print(f"[Auth] Token refreshed and saved.")
        except Exception as e:
            print(f"[Auth] Token refresh failed for {account_id}: {e}")
            return None

    return creds if creds and creds.valid else None

def link_instagram_account(account_id, access_token):
    """
    Links an Instagram account by storing its access token.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (platform, account_id, refresh_token)
            VALUES (?, ?, ?)
            ON CONFLICT(account_id) DO UPDATE SET refresh_token=excluded.refresh_token
        ''', ('instagram', account_id, access_token))
        conn.commit()
    print(f"Successfully linked Instagram account: {account_id}")
