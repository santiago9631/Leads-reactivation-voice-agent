import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def get_credentials():
    """
    Get/refresh Google Calendar API credentials
    """
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def book_appointement(title, description, start):
    """
    Creates an event on Google Calendar
    """
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        # Convert the string to a datetime object
        event_datetime = datetime.fromisoformat(start)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': event_datetime.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (event_datetime + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created successfully. Event ID: {event.get('id')}"

    except HttpError as error:
        return f"An error occurred: {error}"