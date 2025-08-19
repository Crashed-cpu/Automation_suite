import os
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Tuple, Optional, List, Union
import streamlit as st
from io import BytesIO

def generate_gradient(
    size: Tuple[int, int] = (800, 600),
    colors: List[Tuple[int, int, int]] = [(255, 0, 0), (0, 0, 255)],
    direction: str = 'horizontal'
) -> Image.Image:
    """
    Generate a gradient image with the specified colors and direction.
    
    Args:
        size: Width and height of the image (width, height)
        colors: List of RGB tuples for the gradient
        direction: 'horizontal', 'vertical', or 'diagonal'
        
    Returns:
        PIL.Image: Generated gradient image
    """
    # Create a blank image
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    if direction == 'horizontal':
        for x in range(size[0]):
            # Calculate the color at this x position
            ratio = x / size[0]
            r = int(colors[0][0] * (1 - ratio) + colors[-1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[-1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[-1][2] * ratio)
            draw.line([(x, 0), (x, size[1])], fill=(r, g, b))
            
    elif direction == 'vertical':
        for y in range(size[1]):
            # Calculate the color at this y position
            ratio = y / size[1]
            r = int(colors[0][0] * (1 - ratio) + colors[-1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[-1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[-1][2] * ratio)
            draw.line([(0, y), (size[0], y)], fill=(r, g, b))
            
    elif direction == 'diagonal':
        for x in range(size[0]):
            for y in range(size[1]):
                # Calculate the color based on diagonal position
                ratio = (x + y) / (size[0] + size[1])
                r = int(colors[0][0] * (1 - ratio) + colors[-1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[-1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[-1][2] * ratio)
                draw.point((x, y), fill=(r, g, b))
    
    return img

def add_text_to_image(
    img: Image.Image,
    text: str,
    font_size: int = 40,
    text_color: Tuple[int, int, int] = (255, 255, 255),
    position: Tuple[Union[int, str], Union[int, str]] = ('center', 'center')
) -> Image.Image:
    """
    Add text to an image.
    
    Args:
        img: Input image
        text: Text to add
        font_size: Font size
        text_color: Text color as RGB tuple
        position: Position as (x, y) where x and y can be 'left', 'center', 'right' or pixel values
        
    Returns:
        PIL.Image: Image with text added
    """
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load a nice font, fall back to default if not available
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Handle x position
    if position[0] == 'left':
        x = 10
    elif position[0] == 'center':
        x = (img.width - text_width) // 2
    elif position[0] == 'right':
        x = img.width - text_width - 10
    else:
        x = position[0]
    
    # Handle y position
    if position[1] == 'top':
        y = 10
    elif position[1] == 'center':
        y = (img.height - text_height) // 2
    elif position[1] == 'bottom':
        y = img.height - text_height - 10
    else:
        y = position[1]
    
    # Add text with a slight shadow for better visibility
    draw.text((x+1, y+1), text, fill=(0, 0, 0), font=font)
    draw.text((x, y), text, fill=text_color, font=font)
    
    return img

def generate_random_shape(
    img: Image.Image,
    shape_type: str = 'circle',
    color: Optional[Tuple[int, int, int]] = None,
    size_range: Tuple[int, int] = (50, 200)
) -> Image.Image:
    """
    Add a random shape to the image.
    
    Args:
        img: Input image
        shape_type: Type of shape ('circle', 'rectangle', 'triangle')
        color: Shape color as RGB tuple (random if None)
        size_range: Min and max size of the shape
        
    Returns:
        PIL.Image: Image with shape added
    """
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Generate random position and size
    width, height = img.size
    shape_size = random.randint(*size_range)
    x = random.randint(0, width - shape_size)
    y = random.randint(0, height - shape_size)
    
    # Generate random color if not specified
    if color is None:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            128  # Semi-transparent
        )
    
    # Draw the shape
    if shape_type == 'circle':
        draw.ellipse([x, y, x + shape_size, y + shape_size], fill=color)
    elif shape_type == 'rectangle':
        draw.rectangle([x, y, x + shape_size, y + shape_size], fill=color)
    elif shape_type == 'triangle':
        points = [
            (x + shape_size // 2, y),
            (x, y + shape_size),
            (x + shape_size, y + shape_size)
        ]
        draw.polygon(points, fill=color)
    
    return img

def generate_image(
    width: int = 800,
    height: int = 600,
    gradient_colors: List[Tuple[int, int, int]] = [(255, 0, 0), (0, 0, 255)],
    gradient_direction: str = 'horizontal',
    text: Optional[str] = None,
    text_color: Tuple[int, int, int] = (255, 255, 255),
    font_size: int = 40,
    shapes_count: int = 5,
    shape_types: List[str] = ['circle', 'rectangle', 'triangle']
) -> Image.Image:
    """
    Generate a custom image with gradient background, text, and shapes.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        gradient_colors: List of RGB tuples for the gradient
        gradient_direction: 'horizontal', 'vertical', or 'diagonal'
        text: Optional text to add to the image
        text_color: Text color as RGB tuple
        font_size: Font size for the text
        shapes_count: Number of random shapes to add
        shape_types: List of shape types to use ('circle', 'rectangle', 'triangle')
        
    Returns:
        PIL.Image: Generated image
    """
    # Generate gradient background
    img = generate_gradient(
        size=(width, height),
        colors=gradient_colors,
        direction=gradient_direction
    )
    
    # Add random shapes
    for _ in range(shapes_count):
        shape_type = random.choice(shape_types)
        img = generate_random_shape(img, shape_type=shape_type)
    
    # Add text if provided
    if text:
        img = add_text_to_image(
            img,
            text=text,
            font_size=font_size,
            text_color=text_color,
            position=('center', 'center')
        )
    
    return img

def get_image_controls():
    """
    Returns the image generation controls and their values.
    Shows controls when on the image generator tab and the checkbox is checked.
    """
    # Only show controls if we're on the image generator tab
    if st.session_state.get('active_tab') != 'image_generator':
        return {}
    
    # Initialize the show_controls state if it doesn't exist (default to False)
    if 'show_img_controls' not in st.session_state:
        st.session_state.show_img_controls = False
    
    # Add a checkbox to toggle controls
    show_controls = st.sidebar.checkbox(
        "⚙️ Show Image Controls",
        value=st.session_state.show_img_controls,
        key='show_img_controls_checkbox',
        on_change=lambda: setattr(st.session_state, 'show_img_controls', 
                               not st.session_state.show_img_controls)
    )
    
    # Only show controls if checkbox is checked
    if not st.session_state.show_img_controls:
        return {}
        
    controls = {}
    
    # Use columns to better organize the controls
    with st.sidebar.expander("🛠️ Image Settings", expanded=True):
        st.markdown("### 🎨 Image Settings")
        controls['width'] = st.slider("Width", 100, 1920, 800, 10)
        controls['height'] = st.slider("Height", 100, 1080, 600, 10)
        
        st.markdown("### 🌈 Gradient")
        controls['gradient_type'] = st.selectbox(
            "Gradient Direction",
            ["Horizontal", "Vertical", "Diagonal"]
        ).lower()
        
        col1, col2 = st.columns(2)
        with col1:
            controls['color1'] = st.color_picker("Color 1", "#FF0000")
        with col2:
            controls['color2'] = st.color_picker("Color 2", "#0000FF")
        
        st.markdown("### ✏️ Text (Optional)")
        controls['text'] = st.text_input("Text")
        if controls['text']:
            controls['text_color'] = st.color_picker("Text Color", "#FFFFFF")
            controls['font_size'] = st.slider("Font Size", 10, 200, 60)
        else:
            controls['text_color'] = "#FFFFFF"
            controls['font_size'] = 40
        
        st.markdown("### 🔷 Shapes")
        controls['shapes_count'] = st.slider("Number of Shapes", 0, 20, 5)
        controls['shape_types'] = st.multiselect(
            "Shape Types",
            ["Circle", "Rectangle", "Triangle"],
            ["Circle", "Rectangle", "Triangle"]
        )
        
        controls['generate_btn'] = st.button("🎨 Generate Image")
    
    return controls

def image_generation_ui():
    """
    Streamlit UI for the image generation tool.
    """
    st.markdown("## 🖼️ Image Generation")
    
    # Only show controls in the sidebar when this tab is active
    controls = get_image_controls()
    
    # Show a message if no controls are visible (tab not active yet)
    if not controls:
        st.info("👈 Select the '🎨 Image Generator' tab to see the controls")
        return
    
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Process the controls
    colors = [hex_to_rgb(controls['color1']), hex_to_rgb(controls['color2'])]
    shape_types = [s.lower() for s in controls['shape_types']]
    text = controls['text'] if controls['text'] else None
    text_color = hex_to_rgb(controls['text_color'].lstrip('#')) if text else (255, 255, 255)
    
    if controls['generate_btn'] or 'last_image' not in st.session_state:
        # Generate the image
        img = generate_image(
            width=controls['width'],
            height=controls['height'],
            gradient_colors=colors,
            gradient_direction=controls['gradient_type'],
            text=text,
            text_color=text_color,
            font_size=controls['font_size'],
            shapes_count=controls['shapes_count'],
            shape_types=shape_types
        )
        
        # Save to session state
        st.session_state.last_image = img
    else:
        img = st.session_state.last_image if 'last_image' in st.session_state else None
    
    if img is None:
        st.info("👈 Use the sidebar controls to generate your first image!")
        return
    
    # Display the image
    st.image(img, use_column_width=True)
    
    # Download button
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    st.download_button(
        label="⬇️ Download Image",
        data=buffered.getvalue(),
        file_name="generated_image.png",
        mime="image/png"
    )

if __name__ == "__main__":
    image_generation_ui()
