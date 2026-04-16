# Email & Calendar Automation Skill

## Fuente
ComposioHQ/awesome-claude-skills (Gmail, Outlook, Calendar), VoltAgent/awesome-agent-skills

---

## Email: IMAP/SMTP (Universal)

```python
import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import os

class EmailClient:
    def __init__(self, 
                 imap_host: str, smtp_host: str,
                 email_addr: str, password: str,
                 imap_port: int = 993, smtp_port: int = 587):
        self.imap_host = imap_host
        self.smtp_host = smtp_host
        self.email_addr = email_addr
        self.password = password
        self.imap_port = imap_port
        self.smtp_port = smtp_port

    def _decode_header_value(self, value: str) -> str:
        decoded_parts = decode_header(value)
        result = ""
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                result += part.decode(charset or 'utf-8', errors='replace')
            else:
                result += part
        return result

    def list_unread(self, folder: str = 'INBOX', limit: int = 20) -> list[dict]:
        with imaplib.IMAP4_SSL(self.imap_host, self.imap_port) as imap:
            imap.login(self.email_addr, self.password)
            imap.select(folder)
            
            _, msg_ids = imap.search(None, 'UNSEEN')
            ids = msg_ids[0].split()[-limit:]
            
            emails = []
            for msg_id in ids:
                _, data = imap.fetch(msg_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                emails.append({
                    'id': msg_id.decode(),
                    'from': self._decode_header_value(msg.get('From', '')),
                    'subject': self._decode_header_value(msg.get('Subject', '')),
                    'date': msg.get('Date', ''),
                    'body': self._get_body(msg)
                })
            return emails

    def _get_body(self, msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode('utf-8', errors='replace')
        return msg.get_payload(decode=True).decode('utf-8', errors='replace')

    def send_email(self, to: str | list, subject: str, body: str,
                   html_body: str = None, attachments: list = None,
                   cc: str = None, bcc: str = None):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_addr
        msg['To'] = to if isinstance(to, str) else ', '.join(to)
        msg['Subject'] = subject
        if cc: msg['Cc'] = cc
        if bcc: msg['Bcc'] = bcc

        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        if attachments:
            for filepath in attachments:
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
                msg.attach(part)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_addr, self.password)
            server.sendmail(self.email_addr, 
                           [to] if isinstance(to, str) else to, 
                           msg.as_string())

    def mark_as_read(self, msg_id: str, folder: str = 'INBOX'):
        with imaplib.IMAP4_SSL(self.imap_host, self.imap_port) as imap:
            imap.login(self.email_addr, self.password)
            imap.select(folder)
            imap.store(msg_id, '+FLAGS', '\\Seen')

    def search_emails(self, query: str, folder: str = 'INBOX') -> list:
        """IMAP search criteria: FROM, SUBJECT, BODY, SINCE, BEFORE, etc."""
        with imaplib.IMAP4_SSL(self.imap_host, self.imap_port) as imap:
            imap.login(self.email_addr, self.password)
            imap.select(folder)
            _, msg_ids = imap.search(None, query)
            return msg_ids[0].split()
```

---

## Configuraciones IMAP/SMTP por Proveedor

```python
EMAIL_PROVIDERS = {
    'gmail': {
        'imap_host': 'imap.gmail.com',
        'smtp_host': 'smtp.gmail.com',
        'imap_port': 993,
        'smtp_port': 587,
        'note': 'Use App Password (not regular password) if 2FA enabled'
    },
    'outlook': {
        'imap_host': 'outlook.office365.com',
        'smtp_host': 'smtp.office365.com',
        'imap_port': 993,
        'smtp_port': 587
    },
    'yahoo': {
        'imap_host': 'imap.mail.yahoo.com',
        'smtp_host': 'smtp.mail.yahoo.com',
        'imap_port': 993,
        'smtp_port': 587
    },
    'protonmail': {
        'imap_host': '127.0.0.1',  # ProtonMail Bridge
        'smtp_host': '127.0.0.1',
        'imap_port': 1143,
        'smtp_port': 1025
    }
}

# Uso
client = EmailClient(
    **EMAIL_PROVIDERS['gmail'],
    email_addr=os.environ['EMAIL'],
    password=os.environ['EMAIL_APP_PASSWORD']
)
```

---

## Templates de Email HTML

```python
def create_html_email(subject: str, content: str, 
                      cta_text: str = None, cta_url: str = None) -> str:
    """Generate professional HTML email."""
    cta_button = f"""
    <tr>
        <td align="center" style="padding: 30px 0;">
            <a href="{cta_url}" style="
                background-color: #6366F1;
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
            ">{cta_text}</a>
        </td>
    </tr>""" if cta_text and cta_url else ""
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table width="600" cellpadding="0" cellspacing="0" style="
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <!-- Header -->
                    <tr>
                        <td style="
                            background: linear-gradient(135deg, #6366F1, #8B5CF6);
                            padding: 32px;
                            border-radius: 12px 12px 0 0;
                            text-align: center;
                        ">
                            <h1 style="color: white; margin: 0; font-size: 24px;">{subject}</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 32px;">
                            <div style="color: #374151; font-size: 16px; line-height: 1.6;">
                                {content}
                            </div>
                        </td>
                    </tr>
                    {cta_button}
                    <!-- Footer -->
                    <tr>
                        <td style="
                            border-top: 1px solid #e5e7eb;
                            padding: 24px 32px;
                            text-align: center;
                            color: #9ca3af;
                            font-size: 13px;
                        ">
                            Este email fue generado automáticamente por ideas-brillantes
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
```

---

## Calendar: iCalendar (Universal)

```python
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

class iCalendarManager:
    def create_event_ics(self, 
                         title: str,
                         start: datetime,
                         end: datetime,
                         description: str = '',
                         location: str = '',
                         attendees: list = None,
                         timezone: str = 'Europe/Madrid') -> bytes:
        """Create .ics file for any calendar app."""
        cal = Calendar()
        cal.add('prodid', '-//ideas-brillantes//ES')
        cal.add('version', '2.0')
        
        tz = pytz.timezone(timezone)
        event = Event()
        event.add('summary', title)
        event.add('dtstart', tz.localize(start))
        event.add('dtend', tz.localize(end))
        event.add('description', description)
        event.add('location', location)
        
        if attendees:
            for attendee_email in attendees:
                event.add('attendee', f'mailto:{attendee_email}')
        
        cal.add_component(event)
        return cal.to_ical()

    def save_event(self, event_bytes: bytes, output_path: str):
        with open(output_path, 'wb') as f:
            f.write(event_bytes)

    def parse_ics_file(self, ics_path: str) -> list[dict]:
        with open(ics_path, 'rb') as f:
            cal = Calendar.from_ical(f.read())
        
        events = []
        for component in cal.walk():
            if component.name == 'VEVENT':
                events.append({
                    'title': str(component.get('SUMMARY', '')),
                    'start': component.get('DTSTART').dt,
                    'end': component.get('DTEND').dt,
                    'description': str(component.get('DESCRIPTION', '')),
                    'location': str(component.get('LOCATION', ''))
                })
        return events
```

---

## Email Summarization Workflow

```python
async def summarize_unread_emails(email_client: EmailClient, 
                                   ai_client, 
                                   limit: int = 30) -> str:
    """Read unread emails and generate AI summary."""
    emails = email_client.list_unread(limit=limit)
    
    if not emails:
        return "📭 No hay emails sin leer."
    
    email_text = "\n\n---\n\n".join([
        f"De: {e['from']}\nAsunto: {e['subject']}\nFecha: {e['date']}\n{e['body'][:500]}"
        for e in emails
    ])
    
    summary = await ai_client.complete(f"""
    Summarize these {len(emails)} unread emails concisely.
    Group by priority (URGENT first, then important, then informational).
    For each email: sender, subject, one-line summary.
    
    Emails:
    {email_text}
    """)
    
    return f"📧 **{len(emails)} emails sin leer**\n\n{summary}"
```

---

## Plantillas de Email Comunes

```python
EMAIL_TEMPLATES = {
    'meeting_request': """
Hola {name},

Te escribo para solicitar una reunión para hablar sobre {topic}.

¿Estarías disponible {proposed_times}?

La reunión tomaría aproximadamente {duration} minutos.

Quedo a tu disposición para ajustar el horario que mejor te convenga.

Saludos,
{sender_name}
""",
    'follow_up': """
Hola {name},

Me permito hacer seguimiento a {topic} que discutimos el {date}.

¿Has tenido oportunidad de revisarlo? Estoy disponible para resolver cualquier duda.

Saludos,
{sender_name}
""",
    'project_update': """
Hola equipo,

Actualización del proyecto {project_name}:

✅ Completado: {completed}
🔄 En progreso: {in_progress}
⏳ Pendiente: {pending}

Próximos pasos: {next_steps}

Cualquier duda, estoy disponible.

{sender_name}
"""
}
```
