# Google Workspace Integration Skill

## Fuente
ComposioHQ/awesome-claude-skills (Google integrations), VoltAgent/awesome-agent-skills

---

## Setup OAuth2

```python
# credentials.json: descargado desde Google Cloud Console
# Scope mínimos necesarios:
SCOPES = {
    'gmail':     'https://www.googleapis.com/auth/gmail.modify',
    'drive':     'https://www.googleapis.com/auth/drive',
    'sheets':    'https://www.googleapis.com/auth/spreadsheets',
    'calendar':  'https://www.googleapis.com/auth/calendar',
    'docs':      'https://www.googleapis.com/auth/documents',
    'slides':    'https://www.googleapis.com/auth/presentations',
}
```

```bash
pip install google-auth-oauthlib google-api-python-client gspread
```

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

def get_credentials(scopes: list) -> Credentials:
    creds = None
    token_file = f'~/.ideas-brillantes/google_token.pickle'
    token_file = os.path.expanduser(token_file)
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
    
    return creds
```

---

## Gmail

```python
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

class GmailService:
    def __init__(self):
        creds = get_credentials(['https://www.googleapis.com/auth/gmail.modify'])
        self.service = build('gmail', 'v1', credentials=creds)

    def list_unread(self, limit: int = 20) -> list:
        results = self.service.users().messages().list(
            userId='me',
            q='is:unread in:inbox',
            maxResults=limit
        ).execute()
        
        emails = []
        for msg in results.get('messages', []):
            detail = self.service.users().messages().get(
                userId='me', id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in detail['payload']['headers']}
            emails.append({
                'id': msg['id'],
                'from': headers.get('From'),
                'subject': headers.get('Subject'),
                'date': headers.get('Date')
            })
        return emails

    def send_email(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        self.service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()

    def get_email_body(self, message_id: str) -> str:
        msg = self.service.users().messages().get(
            userId='me', id=message_id, format='full').execute()
        
        parts = msg['payload'].get('parts', [msg['payload']])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ''

    def mark_as_read(self, message_id: str):
        self.service.users().messages().modify(
            userId='me', id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    def search(self, query: str, limit: int = 10) -> list:
        """Gmail search syntax: from:user@email.com, subject:hello, after:2025/01/01"""
        results = self.service.users().messages().list(
            userId='me', q=query, maxResults=limit
        ).execute()
        return results.get('messages', [])
```

---

## Google Drive

```python
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

class GoogleDriveService:
    def __init__(self):
        creds = get_credentials(['https://www.googleapis.com/auth/drive'])
        self.service = build('drive', 'v3', credentials=creds)

    def upload_file(self, local_path: str, folder_id: str = None, 
                    mime_type: str = None) -> str:
        """Upload file and return Drive file ID."""
        import mimetypes
        
        name = os.path.basename(local_path)
        mime = mime_type or mimetypes.guess_type(local_path)[0] or 'application/octet-stream'
        
        metadata = {'name': name}
        if folder_id:
            metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(local_path, mimetype=mime, resumable=True)
        file = self.service.files().create(
            body=metadata, media_body=media, fields='id'
        ).execute()
        
        return file.get('id')

    def download_file(self, file_id: str, output_path: str):
        request = self.service.files().get_media(fileId=file_id)
        with io.FileIO(output_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    def list_files(self, folder_id: str = None, query: str = None) -> list:
        q = "trashed=false"
        if folder_id:
            q += f" and '{folder_id}' in parents"
        if query:
            q += f" and name contains '{query}'"
        
        results = self.service.files().list(
            q=q,
            fields="files(id, name, mimeType, size, modifiedTime)"
        ).execute()
        return results.get('files', [])

    def create_folder(self, name: str, parent_id: str = None) -> str:
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            metadata['parents'] = [parent_id]
        
        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')

    def share_file(self, file_id: str, email: str, role: str = 'reader'):
        """role: reader, writer, commenter"""
        permission = {'type': 'user', 'role': role, 'emailAddress': email}
        self.service.permissions().create(fileId=file_id, body=permission).execute()
```

---

## Google Sheets

```python
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

class GoogleSheetsService:
    def __init__(self):
        creds = get_credentials(['https://www.googleapis.com/auth/spreadsheets'])
        self.client = gspread.authorize(creds)

    def read_sheet(self, spreadsheet_id: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        data = sheet.get_all_records()
        return pd.DataFrame(data)

    def write_dataframe(self, df: pd.DataFrame, spreadsheet_id: str, 
                        sheet_name: str = 'Sheet1', clear_first: bool = True):
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        
        if clear_first:
            sheet.clear()
        
        # Headers + data
        values = [df.columns.tolist()] + df.values.tolist()
        sheet.update('A1', values)

    def append_row(self, spreadsheet_id: str, row: list, sheet_name: str = 'Sheet1'):
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_row(row)

    def create_spreadsheet(self, title: str) -> str:
        spreadsheet = self.client.create(title)
        return spreadsheet.id

    def update_cell(self, spreadsheet_id: str, cell: str, value, sheet_name: str = 'Sheet1'):
        """cell: 'A1', 'B5', etc."""
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.update_acell(cell, value)
```

---

## Google Calendar

```python
from datetime import datetime, timedelta

class GoogleCalendarService:
    def __init__(self):
        creds = get_credentials(['https://www.googleapis.com/auth/calendar'])
        self.service = build('calendar', 'v3', credentials=creds)

    def list_events(self, days_ahead: int = 7, calendar_id: str = 'primary') -> list:
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
        
        events = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now, timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events.get('items', [])

    def create_event(self, title: str, start: datetime, end: datetime,
                     description: str = '', attendees: list = None,
                     location: str = '', calendar_id: str = 'primary') -> str:
        event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {'dateTime': start.isoformat(), 'timeZone': 'Europe/Madrid'},
            'end': {'dateTime': end.isoformat(), 'timeZone': 'Europe/Madrid'},
            'reminders': {'useDefault': True}
        }
        
        if attendees:
            event['attendees'] = [{'email': e} for e in attendees]
        
        result = self.service.events().insert(
            calendarId=calendar_id, body=event
        ).execute()
        
        return result.get('id')

    def delete_event(self, event_id: str, calendar_id: str = 'primary'):
        self.service.events().delete(
            calendarId=calendar_id, eventId=event_id
        ).execute()
```

---

## Google Docs

```python
class GoogleDocsService:
    def __init__(self):
        creds = get_credentials(['https://www.googleapis.com/auth/documents'])
        self.service = build('docs', 'v1', credentials=creds)

    def create_document(self, title: str) -> str:
        doc = self.service.documents().create(
            body={'title': title}
        ).execute()
        return doc.get('documentId')

    def append_text(self, doc_id: str, text: str):
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': text
            }
        }]
        self.service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

    def get_text(self, doc_id: str) -> str:
        doc = self.service.documents().get(documentId=doc_id).execute()
        content = doc.get('body', {}).get('content', [])
        text = ''
        for element in content:
            if 'paragraph' in element:
                for part in element['paragraph'].get('elements', []):
                    if 'textRun' in part:
                        text += part['textRun'].get('content', '')
        return text
```
