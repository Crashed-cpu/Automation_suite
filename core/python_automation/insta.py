import os
import streamlit as st
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
from dotenv import load_dotenv
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramPoster:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.client = None

    def login(self):
        """Log in to Instagram"""
        try:
            self.client = Client()
            # Try to load session if it exists
            if os.path.exists("instagram_session.json"):
                self.client.load_settings("instagram_session.json")
                self.client.login(self.username, self.password)
                # Update session after successful login
                self.client.dump_settings("instagram_session.json")
            else:
                self.client.login(self.username, self.password)
                self.client.dump_settings("instagram_session.json")
            return True
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def post_image(self, image_path, caption=""):
        """Post an image to Instagram"""
        if not self.client:
            if not self.login():
                return False, "Failed to log in to Instagram"

        try:
            # Upload the image
            media = self.client.photo_upload(
                path=image_path,
                caption=caption
            )
            return True, "Image posted successfully!"
        except LoginRequired:
            # If login is required, try to re-login
            try:
                self.client.login(self.username, self.password)
                media = self.client.photo_upload(
                    path=image_path,
                    caption=caption
                )
                return True, "Image posted successfully after re-login!"
            except Exception as e:
                return False, f"Failed to post after re-login: {str(e)}"
        except Exception as e:
            return False, f"Failed to post image: {str(e)}"

def instagram_ui():
    """Streamlit UI for Instagram posting"""
    st.markdown("## 📸 Instagram Post Automation")
    
    # Check if credentials are set
    if not os.getenv("INSTAGRAM_USERNAME") or not os.getenv("INSTAGRAM_PASSWORD"):
        st.warning("Instagram credentials not found in environment variables. Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in your .env file.")
        return

    poster = InstagramPoster()
    
    # Image upload
    uploaded_file = st.file_uploader("Choose an image to post", type=["jpg", "jpeg", "png"])
    
    # Caption input
    caption = st.text_area("Caption", "Automated post via Automation Suite! 🤖📸 #Automation #Python")
    
    # Post button
    if st.button("Post to Instagram"):
        if not uploaded_file:
            st.error("Please select an image to upload")
            return
            
        # Save uploaded file temporarily
        temp_image = Path("temp_upload.jpg")
        try:
            with open(temp_image, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Show progress
            with st.spinner("Posting to Instagram..."):
                success, message = poster.post_image(str(temp_image), caption)
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
        finally:
            # Clean up temp file
            if temp_image.exists():
                temp_image.unlink()

# For testing when run directly
if __name__ == "__main__":
    instagram_ui()
