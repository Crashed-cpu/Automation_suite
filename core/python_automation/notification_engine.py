import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import pywhatkit as kit
from dotenv import load_dotenv

# Load environment
load_dotenv()
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_SMS_NUM = os.getenv("TWILIO_NUMBER")
TWILIO_MSG_SERVICE_SID = os.getenv("TWILIO_MSG_SERVICE_SID")
TWILIO_WHATSAPP_NUM = os.getenv("TWILIO_WHATSAPP_NUM")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

client = Client(TWILIO_SID, TWILIO_TOKEN)

def sanitize_number(num):
    num = str(num).strip().replace(' ', '').replace('\u200b', '')
    return num if num.startswith('+') else '+91' + num[-10:]

def load_templates(path):
    templates = {}
    with open(path, 'r') as f:
        key = None
        for line in f:
            line = line.strip()
            if line.startswith('['):
                key = line[1:-1]
                templates[key] = ''
            elif key:
                templates[key] += line + '\n'
    return templates

def send_email(to_email, subject, message, from_email=EMAIL_ADDRESS, password=EMAIL_PASSWORD):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()

        print(f"[Email] Sent to {to_email}")
    except Exception as e:
        print(f"[Email Error] {to_email}: {e}")

def send_instant_whatsapp(number, message):
    try:
        number = sanitize_number(number)
        kit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
        print(f"[WhatsApp Instant] Sent to {number}")
    except Exception as e:
        print(f"[WhatsApp Error] {number}: {e}")

def send_bulk_sms(number, message, use_service=False):
    try:
        number = sanitize_number(number)
        if use_service:
            client.messages.create(messaging_service_sid=TWILIO_MSG_SERVICE_SID, to=number, body=message)
        else:
            client.messages.create(from_=TWILIO_SMS_NUM, to=number, body=message)
        print(f"[SMS] Sent to {number}")
    except Exception as e:
        print(f"[SMS Error] {number}: {e}")

def send_whatsapp_twilio(number, message):
    try:
        number = sanitize_number(number)
        client.messages.create(from_=f"whatsapp:{TWILIO_WHATSAPP_NUM}", to=f"whatsapp:{number}", body=message)
        print(f"[Twilio WhatsApp] Sent to {number}")
    except Exception as e:
        print(f"[Twilio WhatsApp Error] {number}: {e}")

def send_voice_call(number, audio_url):
    try:
        number = sanitize_number(number)
        twiml = f'<Response><Play>{audio_url}</Play></Response>'
        client.calls.create(twiml=twiml, from_=TWILIO_SMS_NUM, to=number)
        print(f"[Voice Call] Sent to {number}")
    except Exception as e:
        print(f"[Voice Call Error] {number}: {e}")

def get_notification_options():
    """Return a dictionary of notification options for the UI"""
    return {
        "1": {"label": "📱 SMS Only", "function": "sms"},
        "2": {"label": "💬 WhatsApp Only", "function": "whatsapp"},
        "3": {"label": "📞 Voice Call", "function": "voice"},
        "4": {"label": "📱 + 💬 SMS + WhatsApp", "function": "sms_whatsapp"},
        "5": {"label": "📱 + 📞 SMS + Voice Call", "function": "sms_voice"},
        "6": {"label": "💬 + 📞 WhatsApp + Voice Call", "function": "whatsapp_voice"},
        "7": {"label": "🚀 All Channels", "function": "all"}
    }

def notify_contacts(contacts_df, message_template, audio_url, notification_type):
    """Send notifications based on the selected type"""
    results = []
    
    for _, row in contacts_df.iterrows():
        name = row.get('Name', 'Friend')
        raw_phone = row.get('Phone')
        sms_enabled = str(row.get('SMS', 'True')).lower() == 'true'
        whatsapp_enabled = str(row.get('Whatsapp', 'True')).lower() == 'true'
        message = message_template.format(name=name)
        phone = sanitize_number(raw_phone)
        
        try:
            if notification_type == "sms" and sms_enabled:
                send_bulk_sms(phone, message)
                results.append(f"✅ SMS sent to {name} ({phone})")
                
            elif notification_type == "whatsapp" and whatsapp_enabled:
                send_whatsapp_twilio(phone, message)
                results.append(f"✅ WhatsApp sent to {name} ({phone})")
                
            elif notification_type == "voice":
                send_voice_call(phone, audio_url)
                results.append(f"✅ Voice call to {name} ({phone}) initiated")
                
            elif notification_type == "sms_whatsapp":
                if sms_enabled:
                    send_bulk_sms(phone, message)
                    results.append(f"✅ SMS sent to {name} ({phone})")
                if whatsapp_enabled:
                    send_whatsapp_twilio(phone, message)
                    results.append(f"✅ WhatsApp sent to {name} ({phone})")
                    
            elif notification_type == "sms_voice":
                if sms_enabled:
                    send_bulk_sms(phone, message)
                    results.append(f"✅ SMS sent to {name} ({phone})")
                send_voice_call(phone, audio_url)
                results.append(f"✅ Voice call to {name} ({phone}) initiated")
                
            elif notification_type == "whatsapp_voice":
                if whatsapp_enabled:
                    send_whatsapp_twilio(phone, message)
                    results.append(f"✅ WhatsApp sent to {name} ({phone})")
                send_voice_call(phone, audio_url)
                results.append(f"✅ Voice call to {name} ({phone}) initiated")
                
            elif notification_type == "all":
                if sms_enabled:
                    send_bulk_sms(phone, message)
                    results.append(f"✅ SMS sent to {name} ({phone})")
                if whatsapp_enabled:
                    send_whatsapp_twilio(phone, message)
                    results.append(f"✅ WhatsApp sent to {name} ({phone})")
                send_voice_call(phone, audio_url)
                results.append(f"✅ Voice call to {name} ({phone}) initiated")
                
        except Exception as e:
            results.append(f"❌ Error sending to {name} ({phone}): {str(e)}")
    
    return results

def notify_from_csv(csv_file, template_file, audio_url, notification_type=None):
    """CLI function to send notifications"""
    df = pd.read_csv(csv_file)
    templates = load_templates(template_file)
    message_template = templates.get('default', "Hi {name}, this is your update.")
    
    if notification_type is None:
        # CLI mode
        options = get_notification_options()
        print("\nSelect Notification Mode:")
        for key, option in options.items():
            print(f"{key} - {option['label']}")
        
        choice = input("\nEnter choice number: ").strip()
        if choice in options:
            notification_type = options[choice]["function"]
        else:
            print("Invalid choice!")
            return
    
    return notify_contacts(df, message_template, audio_url, notification_type)

# CLI entry point
if __name__ == "__main__":
    notify_from_csv(
        csv_file="../../data/csv/customers.csv",
        template_file="../../templates/message.txt",
        audio_url="https://www.pacdv.com/sounds/voices/maybe-next-time.wav"
    )