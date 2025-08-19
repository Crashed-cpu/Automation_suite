import os 
import google.generativeai as genai
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import base64
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("API_KEY"))
    API_AVAILABLE = True
except Exception as e:
    API_AVAILABLE = False

# Available Prompting Styles
PROMPT_STYLES = {
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

def show_burnout_assistant():
    """Display the Burnout Recovery Assistant UI"""
    import streamlit as st
    
    # Check if API key is available
    if not API_AVAILABLE:
        st.error("""
        Gemini API key not found. Please ensure you have:
        1. Created a .env file in your project root
        2. Added your Gemini API key like: `API_KEY=your_api_key_here`
        3. Installed required dependencies with `pip install -r requirements.txt`
        """)
        return
        
    st.title("🧘‍♂️ Burnout Recovery Assistant")
        
    st.markdown("""
    Describe your daily routine or symptoms, and choose a style of prompting to generate 
    your personalized wellness strategy. This assistant is designed to help you prevent 
    and recover from burnout by providing tailored advice based on your specific situation.
    """)
    
    with st.expander("ℹ️ How to use this assistant"):
        st.markdown("""
        1. Describe your daily routine, work schedule, or specific symptoms you're experiencing
        2. Choose a prompting style (explained below)
        3. Click 'Generate Recovery Plan' to get personalized advice
        
        **Prompting Styles:**
        - **Zero-shot**: Direct advice based on your input
        - **One-shot**: Advice based on a similar example
        - **Few-shot**: Advice based on multiple examples
        - **Role-based**: Structured advice from a counselor's perspective
        - **Chain-of-thought**: Detailed, step-by-step analysis
        """)

    # User Inputs
    user_input = st.text_area(
        "Your routine", 
        placeholder="e.g., Internship from 8 AM to 10 PM, 18km commute, always sleepy during mentorship...",
        height=150
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        style_choice = st.selectbox("Choose Prompting Style", list(PROMPT_STYLES.keys()))
    
    # Generate Output
    if st.button("Generate Recovery Plan", use_container_width=True):
        if not user_input.strip():
            st.warning("Please describe your routine or symptoms to get personalized advice.")
            return
            
        prompt = PROMPT_STYLES[style_choice](user_input)
        
        with st.spinner("Analyzing your routine and generating personalized advice..."):
            try:
                # Use gemini-2.5-flash model for consistency with prompted_model.py
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content([prompt])  # Note: Using list format to match prompted_model.py
                except Exception as model_error:
                    st.error(f"Failed to generate response: {str(model_error)}")
                    st.info("Please check your API key and ensure you have access to the Gemini API")
                    return
                
                st.markdown("---")
                st.subheader("Your Personalized Wellness Plan")
                st.markdown(f"*Generated using {style_choice} prompting*")
                
                # Display the response with better formatting
                response_text = ""
                if hasattr(response, 'text'):
                    response_text = response.text
                elif hasattr(response, 'result') and hasattr(response.result, 'text'):
                    response_text = response.result.text
                
                # Display the response in a chat-like format
                with st.chat_message("assistant"):
                    st.markdown("### Your Personalized Wellness Plan")
                    st.markdown(f"*Generated using {style_choice} prompting*")
                    st.markdown("---")
                    st.markdown(response_text)
                    st.success("💡 Remember to take breaks and prioritize your well-being!")
                
                # Add download as PDF button below the response
                st.markdown("---")
                st.markdown("### Download Options")
                pdf_path = create_pdf(response_text, style_choice, user_input)
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    b64 = base64.b64encode(pdf_data).decode()
                    
                    # Create a nicer download button
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_data,
                        file_name="burnout_recovery_plan.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error("Failed to generate response. Please check your API key and try again.")
                st.exception(e)

def create_pdf(plan_text, style_used, user_input):
    """Create a PDF file with the generated wellness plan"""
    try:
        # Create PDF object with smaller margins
        pdf = FPDF()
        pdf.add_page()
        
        # Set font and margins
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(left=20, top=20, right=20)
        
        # Try to use Arial Unicode MS if available, otherwise fall back to Arial
        try:
            pdf.set_font('Arial', '', 11)
            # Test if the font supports common special characters
            test_text = "Test: – — •"
            if pdf.get_string_width(test_text) == 0:  # If test fails, try Arial Unicode MS
                pdf.add_font('ArialUnicode', '', 'c:/windows/fonts/arialuni.ttf', uni=True)
                pdf.set_font('ArialUnicode', '', 11)
        except:
            # Fall back to basic Arial if anything goes wrong
            pdf.set_font('Arial', '', 11)
        
        # Add title
        try:
            pdf.set_font('Arial', 'B', 16)
        except:
            pdf.set_font('Arial', 'B', 16)  # Fallback
        pdf.cell(0, 10, txt="Personalized Wellness Plan", ln=True, align='C')
        
        # Add date
        try:
            pdf.set_font('Arial', 'I', 10)
        except:
            pdf.set_font('Arial', 'I', 10)  # Fallback
        pdf.cell(0, 8, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        
        # Add style used
        try:
            pdf.set_font('Arial', 'B', 12)
        except:
            pdf.set_font('Arial', 'B', 12)  # Fallback
        pdf.cell(0, 10, txt=f"Prompting Style: {style_used}", ln=True)
        
        # Add user input section
        pdf.ln(5)
        try:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt="Your Input:", ln=True)
            pdf.set_font('Arial', '', 11)
        except:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt="Your Input:", ln=True)
            pdf.set_font('Arial', '', 11)  # Fallback
        
        # Handle user input with proper wrapping
        pdf.multi_cell(0, 6, txt=user_input)
        
        # Add plan section
        pdf.ln(5)
        try:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt="Your Personalized Wellness Plan:", ln=True)
            pdf.set_font('Arial', '', 11)
        except:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt="Your Personalized Wellness Plan:", ln=True)
            pdf.set_font('Arial', '', 11)  # Fallback
        
        # Process each line of the plan
        for line in plan_text.split('\n'):
            line = line.strip()
            if not line:
                pdf.ln(5)  # Add space between paragraphs
                continue
                
            # Handle bullet points and lists
            if line.startswith(('-', '•', '*', '• ')):
                try:
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(10, 6, txt='• ')
                    line = line.lstrip('-•* ').strip()
                except:
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(10, 6, txt='- ')
                    line = line.lstrip('-•* ').strip()
            else:
                try:
                    pdf.set_font('Arial', '', 11)
                except:
                    pdf.set_font('Arial', '', 11)  # Fallback
            
            # Split long lines into multiple lines if needed
            max_width = 170  # Approximate max width in points
            if pdf.get_string_width(line) > max_width:
                words = line.split()
                current_line = []
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    if pdf.get_string_width(test_line) < max_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            pdf.cell(0, 6, txt=' '.join(current_line), ln=True)
                        current_line = [word]
                if current_line:
                    pdf.cell(0, 6, txt=' '.join(current_line), ln=True)
            else:
                pdf.cell(0, 6, txt=line, ln=True)
        
        # Add footer
        pdf.ln(10)
        try:
            pdf.set_font('Arial', 'I', 8)
        except:
            pdf.set_font('Arial', '', 8)  # Fallback to regular if italic not available
        pdf.cell(0, 5, txt="Generated by CommandHub - Burnout Recovery Assistant", ln=True, align='C')
        
        # Save the PDF
        pdf_path = "burnout_recovery_plan.pdf"
        pdf.output(pdf_path)
        return pdf_path
        
    except Exception as e:
        st.error("Failed to generate PDF. Please try again.")
        st.exception(e)
        return None

# For testing when run directly
if __name__ == "__main__":
    show_burnout_assistant()
