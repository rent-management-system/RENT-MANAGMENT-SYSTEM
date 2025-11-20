import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_reset_email(to_email: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset"
    msg["From"] = settings.SMTP_USER
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

    try:
        print(f"Attempting to connect to SMTP server: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            print("SMTP server connected. Attempting to start TLS...")
            server.starttls()  # Upgrade connection to secure
            print(f"TLS started. Attempting to log in as {settings.SMTP_USER}...")
            server.login(settings.SMTP_USER, settings.SMTP_PASS.get_secret_value())
            print("Logged in successfully. Attempting to send message...")
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
