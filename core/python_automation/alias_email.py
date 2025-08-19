import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional, List, Union

class EmailSender:
    def __init__(self, from_email: str, email_password: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize the email sender with SMTP server details.
        
        Args:
            from_email (str): Your Gmail address
            email_password (str): Your Gmail app password
            smtp_server (str): SMTP server address (default: smtp.gmail.com)
            smtp_port (int): SMTP server port (default: 587 for TLS)
        """
        self.from_email = from_email
        self.email_password = email_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        body: str,
        display_name: str,
        is_html: bool = False
    ) -> bool:
        """
        Send an email using the provided credentials with a display name.
        
        Args:
            to_emails (str or list): Recipient email address(es)
            subject (str): Email subject
            body (str): Email body content
            display_name (str): The name to display instead of the real email
            is_html (bool): Whether the body contains HTML (default: False)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = f'"{display_name}" <{self.from_email}>'
            msg['To'] = ', '.join(to_emails) if isinstance(to_emails, list) else to_emails
            msg['Subject'] = subject
            
            # Attach the body
            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.from_email, self.email_password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

# Example usage (for testing only):
if __name__ == "__main__":
    # Load credentials from environment variables
    from_email = os.getenv('FROM_EMAIL')
    email_password = os.getenv('EMAIL_APP_PASSWORD')
    
    if not from_email or not email_password:
        print("Error: Email credentials not found in environment variables.")
        print("Please set the following environment variables:")
        print("  - FROM_EMAIL: Your Gmail address")
        print("  - EMAIL_APP_PASSWORD: Your Gmail app password")
    else:
        try:
            # Initialize the email sender
            sender = EmailSender(from_email=from_email, email_password=email_password)
            
            # Example: Send a test email
            success = sender.send_email(
                to_emails=os.getenv('TEST_EMAIL', ''),
                subject="Test Email with Alias",
                body="This is a test email sent with an alias name!",
                display_name="Automation Suite"
            )
            
            if success:
                print("✅ Test email sent successfully!")
            else:
                print("❌ Failed to send test email.")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")