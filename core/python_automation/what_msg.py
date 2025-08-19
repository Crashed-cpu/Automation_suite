import os
import time
import pywhatkit
import streamlit as st
from typing import Optional, List
from datetime import datetime, timedelta
import pandas as pd

# Environment variables for configuration
WHATSAPP_WEB_LOAD_TIME = int(os.getenv('WHATSAPP_WEB_LOAD_TIME', '10'))  # seconds to wait for WhatsApp Web to load
MESSAGE_DELAY = int(os.getenv('MESSAGE_DELAY', '15'))  # seconds between messages

def format_phone_number(phone_number: str) -> str:
    """
    Format phone number to ensure it has proper country code.
    
    Args:
        phone_number: Phone number to format
        
    Returns:
        str: Formatted phone number with country code
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone_number))
    
    # If number starts with country code (India: 91), add +
    if digits.startswith('91') and len(digits) > 10:
        return '+' + digits
    # If number is 10 digits (Indian number without country code), add +91
    elif len(digits) == 10:
        return '+91' + digits
    # If already has +, return as is
    elif phone_number.startswith('+'):
        return phone_number
    # Default: assume it's a local number
    return '+91' + digits[-10:]

def send_whatsapp_message(
    phone_number: str,
    message: str,
    wait_time: int = WHATSAPP_WEB_LOAD_TIME,
    tab_close: bool = True
) -> bool:
    """
    Send a WhatsApp message to a phone number.
    
    Args:
        phone_number: Phone number (with or without country code, e.g., '8955477736' or '+918955477736')
        message: Message to send
        wait_time: Seconds to wait for WhatsApp Web to load
        tab_close: Whether to close the tab after sending
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        # Format the phone number
        phone_number = format_phone_number(phone_number)
        
        # Get current time and add delay
        now = datetime.now()
        send_time = now + timedelta(seconds=30)  # Give some buffer time
        
        # Send the message
        pywhatkit.sendwhatmsg(
            phone_no=phone_number,
            message=message,
            time_hour=send_time.hour,
            time_min=send_time.minute + 1,  # Ensure it's in the future
            wait_time=wait_time,
            tab_close=tab_close
        )
        return True
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return False

def send_bulk_messages(
    phone_numbers: List[str],
    message: str,
    delay: int = MESSAGE_DELAY
) -> dict:
    """
    Send WhatsApp messages to multiple phone numbers with a delay between each.
    
    Args:
        phone_numbers: List of phone numbers with country codes
        message: Message to send
        delay: Seconds to wait between messages
        
    Returns:
        dict: Results of the bulk send operation
    """
    results = {
        'total': len(phone_numbers),
        'success': 0,
        'failed': 0,
        'failed_numbers': []
    }
    
    for i, number in enumerate(phone_numbers):
        st.info(f"Sending to {number} ({i+1}/{len(phone_numbers)})...")
        if send_whatsapp_message(number, message):
            results['success'] += 1
            st.success(f"Message sent to {number}")
        else:
            results['failed'] += 1
            results['failed_numbers'].append(number)
            st.error(f"Failed to send to {number}")
        
        # Add delay between messages (except after the last one)
        if i < len(phone_numbers) - 1:
            time.sleep(delay)
    
    return results

def whatsapp_ui():
    """Streamlit UI for WhatsApp messaging."""
    st.title("📱 WhatsApp Message Sender")
    
    # Tabs for different sending methods
    tab1, tab2 = st.tabs(["Single Message", "Bulk Messages"])
    
    with tab1:
        st.header("Send to a Single Number")
        with st.form("single_message_form"):
            col1, col2 = st.columns([1, 3])
            with col1:
                phone = st.text_input("Phone Number (with country code)", 
                                   placeholder="e.g., +1234567890")
            with col2:
                message = st.text_area("Message", 
                                    placeholder="Type your message here...",
                                    height=150)
            
            submitted = st.form_submit_button("💬 Send Message")
            if submitted:
                if not phone or not message:
                    st.warning("Please fill in all fields")
                else:
                    with st.spinner("Sending message..."):
                        if send_whatsapp_message(phone, message):
                            st.success("Message sent successfully!")
    
    with tab2:
        st.header("Send to Multiple Numbers")
        st.info("Upload a CSV file with a 'phone' column containing numbers with country codes.")
        
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'phone' not in df.columns:
                    st.error("CSV must contain a 'phone' column with phone numbers")
                else:
                    st.success(f"Successfully loaded {len(df)} phone numbers")
                    st.dataframe(df.head())
                    
                    message = st.text_area("Message for all recipients",
                                        placeholder="Type your message here...",
                                        height=150)
                    
                    if st.button("📤 Send to All"):
                        if not message:
                            st.warning("Please enter a message")
                        else:
                            with st.spinner("Sending messages..."):
                                results = send_bulk_messages(
                                    df['phone'].astype(str).tolist(),
                                    message
                                )
                                
                                # Show results
                                st.success(f"Sent {results['success']} out of {results['total']} messages successfully!")
                                if results['failed'] > 0:
                                    st.warning(f"Failed to send {results['failed']} messages.")
                                    if st.expander("Show failed numbers"):
                                        st.write(results['failed_numbers'])
            
            except Exception as e:
                st.error(f"Error processing file: {e}")
    
    # Add some usage instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        ### Single Message
        1. Enter the phone number with country code (e.g., +1234567890)
        2. Type your message
        3. Click 'Send Message'
        
        ### Bulk Messages
        1. Prepare a CSV file with a 'phone' column containing numbers with country codes
        2. Upload the CSV file
        3. Enter your message
        4. Click 'Send to All'
        
        ### Important Notes
        - You need to be logged in to WhatsApp Web in your default browser
        - Keep your browser open while sending messages
        - The first time you send a message, you'll need to scan the QR code
        - There's a small delay between messages to avoid rate limiting
        """)

if __name__ == "__main__":
    whatsapp_ui()