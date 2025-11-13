import os, smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        msg = MIMEText("This is a test email from FastAPI")
        msg["Subject"] = "Test Email"
        msg["From"] = SMTP_USER
        msg["To"] = SMTP_USER
        server.send_message(msg)
        print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
