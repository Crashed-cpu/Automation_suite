import cv2
import numpy as np
import streamlit as st
from typing import Tuple, Optional, List
import io
from PIL import Image

def load_image(file) -> Optional[np.ndarray]:
    """Load an image from a file upload and convert it to RGB."""
    if file is None:
        return None
    
    # Read the image file
    image = Image.open(io.BytesIO(file.getvalue()))
    
    # Convert to numpy array
    img = np.array(image)
    
    # Convert to RGB if needed
    if len(img.shape) == 2:  # Grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    elif img.shape[2] == 3:  # Already RGB
        pass
        
    return img

def detect_faces(image: np.ndarray) -> Optional[List[Tuple[int, int, int, int]]]:
    """Detect faces in an image using OpenCV's built-in face detection."""
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        return None
        
    # Convert numpy array to list of tuples (x, y, w, h)
    return [(x, y, w, h) for (x, y, w, h) in faces]

def get_face_mask(image: np.ndarray, face_rect: Tuple[int, int, int, int]) -> np.ndarray:
    """Create a mask for the face using the face rectangle."""
    # Create a black mask
    mask = np.zeros_like(image)
    
    # Get face coordinates
    x, y, w, h = face_rect
    
    # Create an ellipse mask for the face
    center = (x + w//2, y + h//2)
    axes = (int(w * 0.6), int(h * 0.8))  # Adjust these values to better fit the face
    
    # Draw a filled ellipse
    cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)
    
    # Apply some blur to make the edges smoother
    mask = cv2.GaussianBlur(mask, (15, 15), 0)
    
    return mask

def swap_faces(image1: np.ndarray, image2: np.ndarray) -> Optional[np.ndarray]:
    """
    Swap faces between two images using OpenCV's face detection.
    Returns the second image with the face from the first image.
    """
    # Make copies to avoid modifying the original images
    img1 = image1.copy()
    img2 = image2.copy()
    
    # Convert to BGR for OpenCV operations
    img1_bgr = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    img2_bgr = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    
    # Detect faces in both images
    faces1 = detect_faces(img1_bgr)
    faces2 = detect_faces(img2_bgr)
    
    if not faces1 or not faces2:
        return None
    
    # Use the first face found in each image
    x1, y1, w1, h1 = faces1[0]
    x2, y2, w2, h2 = faces2[0]
    
    # Extract face regions (in BGR)
    face_region1 = img1_bgr[y1:y1+h1, x1:x1+w1]
    face_region2 = img2_bgr[y2:y2+h2, x2:x2+w2]
    
    # Resize face1 to match face2's dimensions
    face_region1_resized = cv2.resize(face_region1, (w2, h2), interpolation=cv2.INTER_AREA)
    
    # Create a mask for the face (white on black)
    mask = 255 * np.ones(face_region2.shape, face_region2.dtype)
    
    # Get the center of the face in image2
    center = (x2 + w2 // 2, y2 + h2 // 2)
    
    try:
        # Clone the resized face onto the target image
        output_bgr = cv2.seamlessClone(
            face_region1_resized,  # source (BGR)
            img2_bgr,             # destination (BGR)
            mask,                 # mask
            center,               # center
            cv2.NORMAL_CLONE
        )
        
        # Convert back to RGB for display
        output_rgb = cv2.cvtColor(output_bgr, cv2.COLOR_BGR2RGB)
        return output_rgb
        
    except Exception as e:
        print(f"Error in seamlessClone: {e}")
        return None

def face_swap_ui():
    """Streamlit UI for face swapping."""
    st.title("🎭 Face Swap")
    st.write("Upload two images to swap faces between them.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Image")
        source_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="source")
        
    with col2:
        st.subheader("Target Image")
        target_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="target")
    
    if source_file and target_file:
        # Load images
        source_img = load_image(source_file)
        target_img = load_image(target_file)
        
        if source_img is not None and target_img is not None:
            # Display original images
            col1, col2 = st.columns(2)
            with col1:
                st.image(source_img, caption="Source Image", use_column_width=True)
            with col2:
                st.image(target_img, caption="Target Image", use_column_width=True)
            
            # Swap faces
            if st.button("🔀 Swap Faces"):
                with st.spinner("Swapping faces..."):
                    try:
                        # Make copies to avoid modifying the original images
                        source_copy = source_img.copy()
                        target_copy = target_img.copy()
                        
                        # Perform face swap (images are in RGB format)
                        result = swap_faces(source_copy, target_copy)
                        
                        if result is not None:
                            # Display result (already in RGB format)
                            st.image(result, caption="Result", use_column_width=True)
                            
                            # Add download button
                            result_img = Image.fromarray(result)
                            img_byte_arr = io.BytesIO()
                            result_img.save(img_byte_arr, format='PNG')
                            st.download_button(
                                label="⬇️ Download Result",
                                data=img_byte_arr.getvalue(),
                                file_name="face_swap_result.png",
                                mime="image/png"
                            )
                        else:
                            st.error("Could not detect faces in one or both images. Please try with different images.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.exception(e)

if __name__ == "__main__":
    face_swap_ui()