import streamlit as st
import google.generativeai as genai
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_KEY"))

# Available Prompting Styles
prompt_styles = {
    "Zero-shot": lambda user_input: f"Suggest wellness strategies for the following routine:\n\n{user_input}",
    
    "One-shot": lambda user_input: (
        "Example:\nA student feels mentally exhausted during daily classes.\n"
        "Recovery Tips: Include short walks, hydration reminders, and sleep tracking.\n\n"
        f"Now help someone with this situation:\n{user_input}"
    ),

    "Few-shot": lambda user_input: (
        "Example 1:\nPerson prepping for exams with burnout symptoms.\n"
        "Advice: Pomodoro focus blocks, Sunday digital detox, and deep breathing rituals.\n\n"
        "Example 2:\nIntern with long commute and brain fog.\n"
        "Advice: Light morning stretches, commute audio journaling, post-lunch alert routines.\n\n"
        "Now create a plan for:\n" + user_input
    ),

    "Role-based": lambda user_input: (
        "You are a certified burnout counselor working with college interns.\n"
        f"Your client's routine:\n{user_input}\n"
        "Provide structured guidance with empathy and clarity. Include:\n"
        "- Morning energizers\n- Commute support\n- Focus strategies\n- Evening recovery\n- Weekly rituals"
    ),

    "Chain-of-thought": lambda user_input: (
        f"Let's analyze this situation step-by-step:\n{user_input}\n"
        "Consider the physical, mental, and emotional drain.\n"
        "Now reason through the day and build a wellness plan accordingly."
    ),
}

# Streamlit UI
st.set_page_config(page_title="Burnout Recovery Assistant", layout="centered")
st.title("🧘‍♂️ Burnout Recovery Assistant")
st.markdown("Describe your daily routine or symptoms, and choose a style of prompting to generate your wellness strategy.")

# User Inputs
user_input = st.text_area("Your routine", placeholder="e.g., Internship from 8 AM to 10 PM, 18km commute, always sleepy during mentorship...")
style_choice = st.selectbox("Choose Prompting Style", list(prompt_styles.keys()))

# Generate Output
if st.button("Generate Recovery Plan"):
    if user_input.strip():
        prompt = prompt_styles[style_choice](user_input)
        model = genai.GenerativeModel("gemini-2.5-flash")

        with st.spinner("Thinking deeply..."):
            response = model.generate_content([prompt])
            st.subheader(f"🧭 Wellness Plan ({style_choice} Prompting)")
            st.markdown(response.text)
    else:
        st.warning("Please enter your routine to proceed.")
