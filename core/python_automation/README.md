# Python Automation Modules

This directory contains various Python automation scripts integrated into the main dashboard.

## 📂 Contents

### Notification System
- `notification_engine.py`: Core notification system supporting SMS, WhatsApp, email, and voice calls
- `sms_sender.py`: SMS sending functionality (Twilio integration)
- `whatsapp_sender.py`: WhatsApp message sending
- `voice_broadcast.py`: Voice call broadcasting
- `alias_email.py`: Email sending with alias support

### Web & Data Tools
- `scrap_web.py`: Web scraping tool with dynamic content support
- `gsearch.py`: Programmatic Google search integration
- `pdf_reporter.py`: PDF report generation

### Media Processing
- `img_generation.py`: Custom image generation with gradients
- `swap_face.py`: Face swapping between images

### System Utilities
- `read_ram.py`: System memory analysis tools
- `what_msg.py`: WhatsApp messaging interface

## 🚀 Usage

All modules are integrated into the main Streamlit dashboard. Access them through the Python Automation section.

## ⚙️ Configuration

Set up your environment variables in `.env` file:
```
# Twilio Credentials
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email Settings
FROM_EMAIL=your_email@example.com
EMAIL_APP_PASSWORD=your_email_app_password

# WhatsApp
WHATSAPP_WEB_LOAD_TIME=10
MESSAGE_DELAY=15
```

## 📝 Dependencies

Install required packages:
```bash
pip install -r ../../../requirements.txt
```
