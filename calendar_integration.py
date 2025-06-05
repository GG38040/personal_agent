"""Google Calendar integration for managing events and schedules."""

from datetime import datetime, timedelta
import os.path
from typing import List, Dict, Optional  # Add Optional to imports
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth import get_google_credentials

LOCAL_TIMEZONE = pytz.timezone('America/New_York')  # Adjust to your timezone

def parse_date_time(date_str: str, time_str: Optional[str] = None) -> datetime:
    """
    Parse date and optional time strings into datetime object.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Optional time in HH:MM format
        
    Returns:
        datetime: Parsed datetime object
    """
    if time_str:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    else:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        dt = dt.replace(hour=9)  # Default to 9 AM if no time specified
    
    return LOCAL_TIMEZONE.localize(dt)

def format_event_time(event: Dict) -> str:
    """Format event time for display."""
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    
    if 'T' in start:  # Full datetime
        start_dt = datetime.fromisoformat(start).astimezone(LOCAL_TIMEZONE)
        end_dt = datetime.fromisoformat(end).astimezone(LOCAL_TIMEZONE)
        return f"{start_dt.strftime('%Y-%m-%d %I:%M %p')} to {end_dt.strftime('%I:%M %p')}"
    else:  # All-day event
        return f"All day on {start}"

def get_calendar_service():
    """Initialize and return Calendar service."""
    creds = get_google_credentials()
    return build('calendar', 'v3', credentials=creds)

def add_event(
    summary: str,
    start_time: datetime,
    end_time: Optional[datetime] = None,
    description: Optional[str] = None,
    location: Optional[str] = None
) -> str:
    """Add a new calendar event."""
    if not end_time:
        end_time = start_time + timedelta(hours=1)  # Default 1-hour duration
    
    service = get_calendar_service()
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': LOCAL_TIMEZONE.zone
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': LOCAL_TIMEZONE.zone
        }
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"
    except HttpError as error:
        return f"Error creating event: {error}"

def delete_event(event_id: str) -> str:
    """Delete a calendar event by ID."""
    service = get_calendar_service()
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return "Event deleted successfully"
    except HttpError as error:
        return f"Error deleting event: {error}"

def list_upcoming_events(max_results: int = 10, days_ahead: int = 7) -> List[Dict]:
    """List upcoming calendar events."""
    service = get_calendar_service()
    now = datetime.utcnow()
    time_max = (now + timedelta(days=days_ahead)).isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except HttpError as error:
        logging.error("Error fetching events: %s", error)
        return []

def search_events(
    query: str,
    max_results: int = 10,
    time_min: Optional[datetime] = None
) -> List[Dict]:
    """Search for calendar events."""
    service = get_calendar_service()
    if not time_min:
        time_min = datetime.utcnow()
    
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
            q=query
        ).execute()
        return events_result.get('items', [])
    except HttpError as error:
        logging.error("Error searching events: %s", error)
        return []