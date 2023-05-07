import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import ipdb
import base64

from dotenv import load_dotenv

load_dotenv()

gcp_client_id=os.environ.get('GCP_CLIENT_ID')
gcp_client_id=os.environ.get('GCP_CLIENT_SECRET')

import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# Set the path to the credentials file
credentials_file = '/Users/taylorcurran/work/handling-support/client_secret_1003414831868-b327q2gbqe534hibsrdubi3u9f07lle5.apps.googleusercontent.com.json'

# Define the Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_header_value(headers, header_name):
    for header in headers:
        if header['name'].lower() == header_name.lower():
            return header['value']
    return None

def get_email_body(payload):
    if 'parts' in payload:
        parts = payload['parts']
        for part in parts:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    text = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    return text
                else:
                    continue
            elif part['mimeType'] == 'multipart/alternative':
                return get_email_body(part)
    else:
        if payload['mimeType'] == 'text/plain':
            if 'data' in payload['body']:
                text = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
                return text
    return None


def main():
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        query = "label:test-label"
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
            print("Messages:")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()

                headers = msg['payload']['headers']
                subject = get_header_value(headers, 'subject')
                from_email = get_header_value(headers, 'From')
                date = get_header_value(headers, 'Date')
                body = get_email_body(msg['payload'])

                if subject is not None:
                    print(f"Subject: {subject}")
                else:
                    print("Subject: Not available")

                if from_email is not None:
                    print(f"From: {from_email}")
                else:
                    print("From: Not available")

                if date is not None:
                    print(f"Date: {date}")
                else:
                    print("Date: Not available")

                if body is not None:
                    print("Body:")
                    print(body)
                else:
                    print("Body: Not available")

                print('-' * 40)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()


# TODO: ontab of how to auth gmail api https://www.one-tab.com/page/V13pHNoLR7q9sFLQ0YDFlg