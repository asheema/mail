import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email(subject, body):
    # Load OAuth 2.0 credentials from client_secret.json
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES
    )
    
    # Use fixed port 8080 to avoid redirect_uri_mismatch
    creds = flow.run_local_server(port=8080)

    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Create EmailMessage object
    message = EmailMessage()
    message.set_content(body)
    message['To'] = os.getenv("TO_EMAIL")       # Set your target email in .env
    message['From'] = "me"
    message['Subject'] = subject

    # Encode message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Create raw message for Gmail API
    create_message = {
        'raw': encoded_message
    }

    # Send the email
    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    return send_message
