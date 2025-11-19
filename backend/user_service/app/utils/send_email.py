import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5174")

def send_reset_email(to_email: str, token: str):
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    html = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}">{reset_link}</a>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
