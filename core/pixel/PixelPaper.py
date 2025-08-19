# PixelPaper
import streamlit as st
import streamlit.components.v1 as components
# Talky
import pyttsx3
import speech_recognition as sr


# --- Page Setup ---
st.set_page_config(layout="wide")
st.title("🧾 PixelPaper - Where ideas render live")

# --- Session State ---
if "html_code" not in st.session_state:
    st.session_state.html_code = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #f4f4f4; font-family: Arial; padding: 20px; }
    h1 { color: #007ACC; }
  </style>
</head>
<body>
  <h1>Welcome!</h1>
  <p>Edit and watch your pixels changing.</p>
</body>
</html>"""

if "preview_height" not in st.session_state:
    st.session_state.preview_height = 400

# --- Utility: RGB to HSL ---
def rgb_to_hsl(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    c_max, c_min = max(r, g, b), min(r, g, b)
    delta = c_max - c_min
    l = (c_max + c_min) / 2
    s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1)) if l not in (0, 1) else 0
    if delta == 0:
        h = 0
    elif c_max == r:
        h = ((g - b) / delta) % 6
    elif c_max == g:
        h = ((b - r) / delta) + 2
    else:
        h = ((r - g) / delta) + 4
    h = int(h * 60)
    return h, int(s * 100), int(l * 100)

# --- Utility: Basic Syntax Checker ---
def simple_html_checker(code):
    errors = []
    tags = ["html", "head", "body", "div", "p", "a", "span", "ul", "li", "table", "tr", "td"]
    for tag in tags:
        open_count = code.lower().count(f"<{tag}")
        close_count = code.lower().count(f"</{tag}>")
        if open_count != close_count:
            errors.append(f"⚠ Tag mismatch: <{tag}> opened {open_count}, closed {close_count}")
    return errors

# --- Sidebar ---
with st.sidebar:
    st.header("⚙ Developer Settings")

    # Upload HTML File
    if st.toggle("📂 Load Existing HTML"):
        st.subheader("📂 Load Existing HTML")
        uploaded_file = st.file_uploader("Upload an HTML file", type=["html"])
        if uploaded_file is not None:
            try:
                st.session_state.html_code = uploaded_file.read().decode("utf-8")
                st.success("✅ HTML loaded into the editor.")
            except Exception as e:
                st.error(f"❌ Failed to read file: {e}")

    # Fullscreen Toggle
    fullscreen = st.toggle("🖥 Full-Width Preview Only")

    # Preview Height
    if st.toggle("📏 Customize Preview Height"):
        st.session_state.preview_height = st.slider(
            "Preview Height", 200, 1000, st.session_state.preview_height
        )

    # Color Picker
    if st.toggle("🎨 Enable Color Picker"):
        color = st.color_picker("Pick a color", "#007ACC")
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        h, s, l = rgb_to_hsl(r, g, b)
        st.markdown("🧾 Snippets for Copying:")
        st.code(f'style="color: {color};"', language="html")
        st.code(f'style="color: rgb({r}, {g}, {b});"', language="html")
        st.code(f'style="color: hsl({h}, {s}%, {l}%);"', language="html")

    # Tag Helper
    if st.toggle("📘 Show HTML Tag Helper"):
        tag = st.selectbox("Choose a tag", ["<img>", "<a>", "<input>", "<button>", "<div>", "<table>"])
        tags = {
            "<img>": {
                "desc": "Embeds an image.",
                "attributes": "src, alt, width, height",
                "example": '<img src="image.png" alt="Description" width="200">'
            },
            "<a>": {
                "desc": "Creates a hyperlink.",
                "attributes": "href, target, rel",
                "example": '<a href="https://example.com" target="_blank">Visit Site</a>'
            },
            "<input>": {
                "desc": "Input field.",
                "attributes": "type, name, value, placeholder",
                "example": '<input type="text" placeholder="Your name">'
            },
            "<button>": {
                "desc": "Clickable button.",
                "attributes": "type, onclick, disabled",
                "example": '<button type="submit">Submit</button>'
            },
            "<div>": {
                "desc": "Generic container.",
                "attributes": "id, class, style",
                "example": '<div class="box">Hello</div>'
            },
            "<table>": {
                "desc": "Table layout.",
                "attributes": "border, cellpadding, cellspacing",
                "example": '<table><tr><td>Cell</td></tr></table>'
            }
        }
        st.write(f"📖 Description:** {tags[tag]['desc']}")
        st.write(f"🔑 Attributes:** {tags[tag]['attributes']}")
        st.code(tags[tag]["example"], language="html")

    # Download
    st.subheader("💾 Export HTML")
    st.download_button("Download index.html", st.session_state.html_code, "index.html", "text/html")

# --- Main Area ---
if fullscreen:
    st.subheader("🔍 Full-Width Preview")
    components.html(st.session_state.html_code, height=st.session_state.preview_height, scrolling=True)

else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍ Edit HTML")
        st.session_state.html_code = st.text_area(
            "Write your HTML code:",
            height=st.session_state.preview_height,
            value=st.session_state.html_code,
            key="editor"
        )

        # Syntax Feedback
        errors = simple_html_checker(st.session_state.html_code)
        if errors:
            with st.expander("⚠ HTML Syntax Warnings", expanded=True):
                for err in errors:
                    st.markdown(f"- {err}")
        else:
            st.caption("✅ No obvious syntax issues.")

    with col2:
        st.subheader("🔍 Live Preview")
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        components.html(st.session_state.html_code, height=st.session_state.preview_height, scrolling=True)


# --- Voice Tools Area ---
st.markdown("---")
st.subheader("🗣️ Talky Voice Tools")

voice_col1, voice_col2 = st.columns(2)

box_style = """
    background-color: #0000;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
"""

with voice_col1:
    st.markdown(f"<div style='{box_style}'>", unsafe_allow_html=True)
    st.markdown("### 🧾 Text to Speech")
    tts_text = st.text_input("Enter text to speak:")
    if st.button("🔊 Speak"):
        if tts_text.strip():
            try:
                engine = pyttsx3.init()
                engine.say(tts_text) # Say first

                engine.runAndWait()
            except RuntimeError:
                # Gracefully recover if loop is already running

                engine.endLoop()
                engine.say(tts_text)
                engine.runAndWait()
            engine.stop()
        else:
            st.warning("Please enter something to speak!")
    st.markdown("</div>", unsafe_allow_html=True)

with voice_col2:
    st.markdown(f"<div style='{box_style}'>", unsafe_allow_html=True)
    st.markdown("### 🎙️ Speech to Text")

    # 👇 Add slight padding above the button to match the input field alignment
    st.markdown("<p style='font-size: 0.8rem; color: white; margin-bottom: 6px;'>Click the button to start listening:</p>", unsafe_allow_html=True)
    
    if st.button("🎧 Start Listening"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please speak now.")
            try:
                audio = recognizer.listen(source, timeout=5)
                result = recognizer.recognize_google(audio)
                st.success("You said:")
                st.write(f"💬 {result}")
            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"🚫 Request error: {e}")
            except sr.WaitTimeoutError:
                st.error("⏳ No speech detected.")
    st.markdown("</div>", unsafe_allow_html=True)