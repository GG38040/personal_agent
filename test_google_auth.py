"""Test script for Google API authentication."""

import logging
from datetime import datetime
from googleapiclient.discovery import build
from google_auth import get_google_credentials

def test_auth():
    """Test Google API authentication and access."""
    print("\n=== Google API Authentication Test ===\n")
    
    try:
        # 1. Test credential acquisition
        print("1. Testing credentials...")
        creds = get_google_credentials()
        if not creds or not creds.valid:
            print("❌ Failed to get valid credentials")
            return
        print("✅ Credentials obtained successfully")

        # 2. Test Gmail API
        print("\n2. Testing Gmail API...")
        gmail = build('gmail', 'v1', credentials=creds)
        profile = gmail.users().getProfile(userId='me').execute()
        print(f"✅ Gmail access verified for: {profile['emailAddress']}")

        # 3. Test Calendar API
        print("\n3. Testing Calendar API...")
        calendar = build('calendar', 'v3', credentials=creds)
        calendar_list = calendar.calendarList().list().execute()
        primary_calendar = next(
            (cal for cal in calendar_list['items'] if cal['primary']),
            None
        )
        if primary_calendar:
            print(f"✅ Calendar access verified for: {primary_calendar['summary']}")
        else:
            print("✅ Calendar API accessible but no primary calendar found")

        print("\n🎉 All authentication tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        logging.error("Auth test failed: %s", str(e))

if __name__ == "__main__":
    test_auth()