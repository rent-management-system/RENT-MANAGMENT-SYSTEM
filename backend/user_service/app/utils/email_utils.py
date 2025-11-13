import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_reset_email(to_email: str, reset_token: str):
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("Missing EMAIL_USER or EMAIL_PASS in .env file")

    reset_link = f"http://localhost:5173/reset-password?token={reset_token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    html = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}" style="color:#1a73e8;">Reset Password</a>
            <br/><br/>
            <p>If you didn’t request this, you can safely ignore this email.</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())