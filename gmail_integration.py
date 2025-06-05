"""Gmail integration module for handling email operations."""

import base64
import os.path
from email.mime.text import MIMEText
from typing import List, Dict, Optional
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth import get_google_credentials

# Define scopes for Gmail API access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]


def get_gmail_service():
    """
    Initialize and return the Gmail service object.
    
    Returns:
        Resource: Gmail API service object
    """
    creds = None
    if os.path.exists('token_gmail.json'):
        creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open('token_gmail.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def send_email(to: str, subject: str, message_text: str) -> dict:
    """
    Send an email using Gmail API.
    
    Args:
        to: Recipient email address
        subject: Email subject
        message_text: Email body content
    
    Returns:
        dict: Response from Gmail API
    """
    service = get_gmail_service()
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}

    try:
        return service.users().messages().send(userId='me', body=body).execute()
    except Exception as e:
        logging.error("Failed to send email: %s", str(e))
        raise


def get_message_details(service, msg_id: str) -> Dict:
    """Get detailed message content."""
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'No Date')

        return {
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'snippet': message.get('snippet', ''),
        }
    except HttpError as error:
        logging.error(f"Error retrieving message {msg_id}: {error}")
        return {}


def list_recent_emails(max_results: int = 10) -> List[Dict]:
    """
    List recent emails from inbox.
    
    Args:
        max_results: Maximum number of emails to retrieve
        
    Returns:
        List[Dict]: List of email details including subject, sender, and snippet
    """
    service = get_gmail_service()
    try:
        # Get list of recent message IDs
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        
        # Get detailed content for each message
        emails = []
        for msg in messages:
            email_data = get_message_details(service, msg['id'])
            if email_data:
                emails.append(email_data)
        
        return emails

    except HttpError as error:
        logging.error(f"Error listing emails: {error}")
        return []


# Update your existing list_emails function to use the new functionality
def list_emails(max_results: int = 10) -> List[Dict]:
    """List recent emails with full details."""
    emails = list_recent_emails(max_results)
    return emails


def search_emails(query: str, max_results: int = 5) -> List[Dict]:
    """Search emails with specific criteria."""
    service = get_gmail_service()
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        return [
            parse_email_content(
                service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
            )
            for msg in messages
        ]
    except Exception as e:
        logging.error("Failed to search emails: %s", str(e))
        raise


def parse_email_content(message_data: dict) -> dict:
    """Extract meaningful information from email content."""
    headers = message_data['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
    
    return {
        'id': message_data['id'],
        'subject': subject,
        'sender': sender,
        'snippet': message_data.get('snippet', ''),
        'date': message_data['internalDate']
    }