import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration
with open("../config/config.json") as f:
    config = json.load(f)

class EmailAgent:
    def __init__(self):
        self.smtp_server = config["email"]["smtp_server"]
        self.port = config["email"]["port"]
        self.sender_email = config["email"]["sender_email"]
        self.password = config["email"]["password"]

    def send_email(self, to_email: str, subject: str, message: str):
        """
        Send an email using Gmail SMTP.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {to_email}")

        except Exception as e:
            print(f"❌ Failed to send email: {e}")

# Example usage — send to yourself
if __name__ == "__main__":
    agent = EmailAgent()
    agent.send_email(
        to_email="adeenzainub@gmail.com",  # sending to yourself
        subject="HubSpot Agent Test Email ✅",
        message="Hey Adeen! 👋\n\nThis is a test email sent from your HubSpot AI agent setup.\n\nIf you received this, your email integration works perfectly! 🚀"
    )
