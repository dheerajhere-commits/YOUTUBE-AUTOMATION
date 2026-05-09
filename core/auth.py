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
            print(f"To link Google account {account_id}, follow the OAuth flow...")
            # For a real implementation, you need client_secret.json
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     'client_secret.json', SCOPES)
            # creds = flow.run_local_server(port=0)

            # Dummy implementation for illustration
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

    # Store in database
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (platform, account_id, refresh_token)
            VALUES (?, ?, ?)
            ON CONFLICT(account_id) DO UPDATE SET refresh_token=excluded.refresh_token
        ''', ('youtube', account_id, 'dummy_refresh_token')) # In real app, creds.refresh_token
        conn.commit()

    print(f"Successfully linked account: {account_id}")
    return creds

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
