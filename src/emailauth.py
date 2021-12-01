import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


class EmailAuth:
    """
    TODO - Logging
    TODO - Test
    Manages Auth with gmail account
    """
    Service = None

    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh auth, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../auth/token.json'):
            creds = Credentials.from_authorized_user_file('../auth/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../auth/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../auth/token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)

    def get_service(self):
        return self.service


if __name__ == '_main__':
    EmailAuth()
