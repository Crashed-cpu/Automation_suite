import os
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import streamlit as st
from core.linux_tools import bash_runner
from core.docker_automation import docker_runner
from core.burnout_assistant import show_burnout_assistant

# Dictionary to hold HTTP server instances by port
http_servers = {}

def start_http_server(port=8000, directory=None):
    """Start a simple HTTP server in a daemon thread on the specified port"""
    global http_servers
    
    # Check if server is already running on this port
    if port in http_servers:
        return True
        
    try:
        # Get the project root directory
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        # If directory is provided, make it relative to project root
        serve_dir = os.path.abspath(os.path.join(project_root, directory)) if directory else project_root
        
        if not os.path.exists(serve_dir):
            st.error(f"Directory not found: {serve_dir}")
            return False
        
        # Create a custom request handler that serves from the specified directory
        class CustomHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=serve_dir, **kwargs)
            
            def log_message(self, format, *args):
                # Suppress logging to keep the console clean
                pass
        
        # Create server in a daemon thread
        def run_server():
            server_address = ('', port)
            httpd = HTTPServer(server_address, CustomHandler)
            http_servers[port] = httpd
            httpd.serve_forever()
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        
        # Give the server a moment to start
        import time
        time.sleep(0.5)
        return True
        
    except Exception as e:
        st.error(f"Failed to start HTTP server on port {port}: {e}")
        if port in http_servers:
            del http_servers[port]
        return False
from core.agentic_ai.streamlit_agentic_assistant import show_agentic_assistant
from core.ui.email_server_ui import show_email_server_page

# ⚙️ Initial Config
st.set_page_config(
    page_title="CommandHub - Menu-Based Automation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sidebar
st.markdown("""
    <link href='https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&display=swap' rel='stylesheet'>
    <style>
        /* Hide specific Streamlit sidebar elements */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Ensure our custom sidebar content is visible */
        [data-testid="stSidebarUserContent"] {
            visibility: visible !important;
        }
        
        /* Style our custom sidebar */
        [data-testid="stSidebar"] {
            padding: 1rem;
        }
        
        .luxury-text {
            font-family: 'Playfair Display', serif;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# Main header with better visual separation
st.markdown(
    """
    <div style='position: relative; text-align: center; background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        <div class='luxury-text' style='position: absolute; right: 20px; top: 12px; text-align: right;'>
            <div style='font-size: 1.1em; font-weight: 700; font-style: italic; color: #2c3e50; text-shadow: 0.5px 0.5px 1px rgba(0,0,0,0.1); line-height: 1.2;'>Ayush Saini</div>
            <div style='font-size: 0.9em; color: #5d6d7e; opacity: 0.9; letter-spacing: 0.5px;'>Team <strong>39</strong></div>
        </div>
        <h1 style='color: #1a1a1a; margin: 0 0 5px 0; font-size: 1.8em; font-weight: 600;'>
            🧠 CommandHub - Menu-Based Automation Dashboard
        </h1>
        <p style='color: #4a4a4a; margin: 0 0 12px 0; font-size: 1.15em; font-weight: 500; letter-spacing: 0.3px;'>
            Unified Control Dashboard
        </p>
        <p style='color: #555; margin: 12px auto 0; font-size: 1em; max-width: 700px; line-height: 1.5;'>
            Welcome to your modular command center. Select a tool from the sidebar to get started.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔐 Session Defaults
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Linux Automation"
if "selected_command" not in st.session_state:
    st.session_state.selected_command = None

# 🧭 Sidebar Tool Navigation
with st.sidebar:
    st.header("🔧 Available Toolsets")

    # Using unique keys for each button to avoid DuplicateWidgetID error
    if st.button("💻 Linux Automation", key="btn_linux"):
        st.session_state.selected_tool = "Linux Automation"
        st.session_state.selected_command = None

    if st.button("🐳 Docker Automation", key="btn_docker"):
        st.session_state.selected_tool = "Docker Automation"
        st.session_state.selected_command = None

    if st.button("🐍 Python Automation", key="btn_python"):
        st.session_state.selected_tool = "Python Automation"
        st.session_state.selected_command = None
        
    if st.button("📊 ML Models", key="btn_ml"):
        st.session_state.selected_tool = "ML Models"
        st.session_state.selected_command = None

    # Add AWS Automation button in the main sidebar with other tools
    if st.button("☁️ AWS Automation", key="btn_aws"):
        st.session_state.selected_tool = "AWS Automation"
        st.session_state.selected_command = None
        
    # Add JavaScript Tools button
    if st.button("🛠️ JavaScript Tools", key="btn_js"):
        st.session_state.selected_tool = "JavaScript Tools"
        st.session_state.selected_command = None
        
    # Add Projects section header
    st.markdown("---")
    st.subheader("🚀 Projects")
    
    # Add Projects under the Projects section
    if st.button("   🧠 Burnout Assistant", key="btn_burnout"):
        st.session_state.selected_tool = "Burnout Assistant"
        st.session_state.selected_command = None
        
    if st.button("   🤖 Agentic AI Assistant", key="btn_agentic_ai"):
        st.session_state.selected_tool = "Agentic AI Assistant"
        st.session_state.selected_command = None
        
    # Add PixelPaper to Projects section
    if st.button("   🎨 PixelPaper", key="btn_pixelpaper"):
        import os
        # Get the full path to PixelPaper.py
        pixelpaper_path = os.path.join(os.path.dirname(__file__), "core", "pixel", "PixelPaper.py")
        # Run the PixelPaper script in a new process
        os.system(f'streamlit run "{pixelpaper_path}"')
        
    # Add Quick Links button (outside Projects section)
    st.markdown("---")
    if st.button("🔗 Quick Links", key="btn_links"):
        st.session_state.selected_tool = "Quick Links"
        st.session_state.selected_command = None
    
    st.markdown("---")
    st.caption("Select a module to begin.")

# Target Configuration (only for Linux and Docker)
if st.session_state.selected_tool in ["Linux Automation", "Docker Automation"]:
    st.markdown("### 🌐 Target Configuration")
    st.text_input("Username", key="username")
    st.text_input("IP Address", key="ip")

# 💻 Linux Automation Module
if st.session_state.selected_tool == "Linux Automation":
    st.markdown("## 💻 Linux Automation")

    commands = list(bash_runner.COMMANDS.keys())
    cols = st.columns(3)

    st.markdown("### 🔍 Select a Command")
    for i, label in enumerate(commands):
        col = cols[i % 3]
        if col.button(label):
            st.session_state.selected_command = label

    if st.session_state.selected_command:
        st.info(f"🧠 Selected command: `{st.session_state.selected_command}`")
        if st.button("🚀 Run Selected Command"):
            user = st.session_state.get("username")
            ip = st.session_state.get("ip")
            if not user or not ip:
                st.warning("Please enter both username and IP address.")
            else:
                with st.spinner(f"Executing `{st.session_state.selected_command}` on {ip}..."):
                    output = bash_runner.run_linux_task(st.session_state.selected_command, user, ip)
                    if output.strip():
                        st.success("✅ Command executed successfully")
                        st.text_area("📄 Output", output, height=300)
                    else:
                        st.error("❌ No output returned or command failed.")
    else:
        st.info("Select a command above to activate the Run button.")

# 🐳 Docker Automation Module
elif st.session_state.selected_tool == "Docker Automation":
    st.markdown("## 🐳 Docker Automation Toolkit")

    docker_cmds = list(docker_runner.DOCKER_COMMANDS.keys())
    cols = st.columns(3)

    # 🔍 Select a Docker Command
    st.markdown("### 🔍 Select a Docker Command")
    for i, label in enumerate(docker_cmds):
        col = cols[i % 3]
        if col.button(label):
            st.session_state.selected_command = label
            st.session_state.command_args = {}
            st.session_state.show_inputs = True

    # 🎯 If command is selected
    selected_label = st.session_state.selected_command
    if selected_label:
        st.info(f"📦 Selected command: `{selected_label}`")

        required_args = docker_runner.DOCKER_COMMAND_INPUTS.get(selected_label, [])
        st.session_state.show_inputs = bool(required_args)
        user = st.session_state.get("username")
        ip = st.session_state.get("ip")

        args = {}
        missing_inputs = []

        # Only show inputs if needed
        if st.session_state.show_inputs:
            input_labels = {
                "name": "🪪 Container Name",
                "image": "📦 Image Name",
                "repo_tag": "🔖 Repo:Tag (e.g., user/app:latest)"
            }

            for arg in required_args:
                args[arg] = st.text_input(input_labels.get(arg, arg.capitalize()))
                if not args[arg]:
                    missing_inputs.append(arg)

        # 🧨 Run button toggles only after command selection
        if st.button("🚀 Run Docker Command"):
            if not user or not ip:
                st.warning("Please enter SSH username and IP address.")
            elif missing_inputs:
                st.warning(f"Missing required input(s): {', '.join(missing_inputs)}")
            else:
                with st.spinner(f"Running `{selected_label}` remotely via SSH..."):
                    output = docker_runner.run_docker_command(selected_label, args, user, ip)
                    if output.strip():
                        st.success("✅ Command executed successfully")
                        st.text_area("📄 Output", output, height=300)
                    else:
                        st.error("❌ No output or command failed.")


# 🐍 Python Automation Module
elif st.session_state.selected_tool == "Python Automation":
    st.markdown("## 🐍 Python Automation")
    
    # Create tabs for different Python automation features
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔔 Notifications",
        "🔍 Google Search",
        "🌐 Web Scraper",
        "📧 Email Sender",
        "🎨 Image Generator",
        "🎭 Face Swap",
        "💬 WhatsApp",
        "📸 Instagram"
    ])
    
    with tab1:
        # Hardcoded values for notifications
        CSV_FILE = "data/csv/customers.csv"
        TEMPLATE_FILE = "templates/message.txt"
        AUDIO_URL = "https://www.pacdv.com/sounds/voices/maybe-next-time.wav"
        
        # Import notification functions
        from core.python_automation.notification_engine import (
            get_notification_options,
            notify_from_csv
        )
        
        st.markdown("### 📱 Notification Options")
        
        # Get notification options
        notification_options = get_notification_options()
        
        # Create a row of buttons for each notification option
        for i in range(0, len(notification_options), 2):
            col1, col2 = st.columns(2)
            with col1:
                if i < len(notification_options):
                    option = notification_options[str(i+1)]
                    if st.button(option["label"], key=f"notif_{i+1}", use_container_width=True):
                        with st.spinner(f"Sending {option['label']}..."):
                            results = notify_from_csv(
                                csv_file=CSV_FILE,
                                template_file=TEMPLATE_FILE,
                                audio_url=AUDIO_URL,
                                notification_type=option["function"]
                            )
                            for result in results:
                                if result.startswith("✅"):
                                    st.success(result)
                                else:
                                    st.error(result)
            
            with col2:
                if i+1 < len(notification_options):
                    option = notification_options[str(i+2)]
                    if st.button(option["label"], key=f"notif_{i+2}", use_container_width=True):
                        with st.spinner(f"Sending {option['label']}..."):
                            results = notify_from_csv(
                                csv_file=CSV_FILE,
                                template_file=TEMPLATE_FILE,
                                audio_url=AUDIO_URL,
                                notification_type=option["function"]
                            )
                            for result in results:
                                if result.startswith("✅"):
                                    st.success(result)
                                else:
                                    st.error(result)
        
        # Compact configuration section
        with st.expander("ℹ️ Notification Configuration", expanded=False):
            st.caption(f"📄 Template: {TEMPLATE_FILE}")
            st.caption(f"📊 Contacts: {CSV_FILE}")
            st.caption(f"🔊 Audio: {AUDIO_URL}")
    
    # Web Search Tab
    with tab2:
        try:
            from core.python_automation.gsearch import search_ui
            search_ui()
        except ImportError as e:
            st.error("Failed to load the search module. Please make sure all dependencies are installed.")
            st.code("pip install googlesearch-python")
            st.exception(e)
    
    # Web Scraper Tab
    with tab3:
        try:
            from core.python_automation.scrap_web import scrape_website_ui
            scrape_website_ui()
        except ImportError as e:
            st.error("Failed to load the web scraper module. Please make sure all dependencies are installed.")
            st.code("pip install beautifulsoup4 requests selenium webdriver-manager")
            st.exception(e)
    
    # Email Sender Tab
    with tab4:
        try:
            from core.python_automation.alias_email import EmailSender
            
            st.markdown("### ✉️ Send Email with Alias")
            
            # Get credentials from environment variables
            from_email = os.getenv('FROM_EMAIL')
            email_password = os.getenv('EMAIL_APP_PASSWORD')
            
            if not from_email or not email_password:
                st.warning("⚠️ Email credentials not found in environment variables.")
                st.info("""
                Please set the following environment variables to use the email sender:
                - `FROM_EMAIL`: Your Gmail address
                - `EMAIL_APP_PASSWORD`: Your Gmail app password
                
                You can create an app password at: https://myaccount.google.com/apppasswords
                """)
            else:
                with st.form("email_form"):
                    # Recipient input
                    to_email = st.text_input("To:", placeholder="recipient@example.com")
                    
                    # Email subject
                    subject = st.text_input("Subject:", placeholder="Your email subject")
                    
                    # Display name (alias)
                    display_name = st.text_input("Display Name:", placeholder="Your Name")
                    
                    # Email body
                    body = st.text_area("Message:", height=200)
                    
                    # Send button
                    if st.form_submit_button("📤 Send Email"):
                        if not all([to_email, subject, body, display_name]):
                            st.error("Please fill in all fields.")
                        else:
                            try:
                                # Initialize the email sender
                                sender = EmailSender(from_email=from_email, email_password=email_password)
                                
                                # Send the email
                                with st.spinner("Sending email..."):
                                    success = sender.send_email(
                                        to_emails=to_email,
                                        subject=subject,
                                        body=body,
                                        display_name=display_name
                                    )
                                    
                                    if success:
                                        st.success("✅ Email sent successfully!")
                                    else:
                                        st.error("❌ Failed to send email. Please check your credentials and try again.")
                                        
                            except Exception as e:
                                st.error(f"❌ Error sending email: {str(e)}")
                                st.exception(e)
        except ImportError as e:
            st.error("Failed to load the email module. Please make sure all dependencies are installed.")
            st.code("pip install python-dotenv")
            st.exception(e)
    
    # Track the active tab in session state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = None
    
    # Image Generator Tab
    with tab5:
        try:
            # Import the image generation UI
            from core.python_automation.img_generation import image_generation_ui
            
            # Set the tab as active in session state
            st.session_state.active_tab = 'image_generator'
            
            # Show the image generation UI
            image_generation_ui()
            
        except ImportError as e:
            st.error("Failed to load the image generation module. Please make sure all dependencies are installed.")
            st.code("pip install pillow numpy")
            st.exception(e)
    
    # Face Swap Tab
    with tab6:
        try:
            # Import the face swap UI
            from core.python_automation.swap_face import face_swap_ui
            
            # Show the face swap UI
            face_swap_ui()
            
        except ImportError as e:
            st.error("Failed to load the face swap module. Please make sure all dependencies are installed.")
            st.code("pip install opencv-python face-recognition numpy")
            st.exception(e)
    
    with tab7:
        try:
            # Import the WhatsApp messaging UI
            from core.python_automation.what_msg import whatsapp_ui
            
            # Show the WhatsApp UI
            whatsapp_ui()
            
        except ImportError as e:
            st.error("Failed to load the WhatsApp messaging module. Please make sure all dependencies are installed.")
            st.code("pip install pywhatkit")
            st.exception(e)
            
    with tab8:
        try:
            # Import the Instagram UI
            from core.python_automation.insta import instagram_ui
            
            # Show the Instagram UI
            instagram_ui()
            
        except ImportError as e:
            st.error("Failed to load the Instagram module. Please make sure all dependencies are installed.")
            st.code("pip install instagrapi python-dotenv")
            st.exception(e)
            
# 🤖 Email Server Section
elif st.session_state.selected_tool == "Email Server":
    show_email_server_page()
    
# ML Models Section
elif st.session_state.selected_tool == "ML Models":
    st.markdown("## 🤖 Machine Learning Models")
    
    # Create tabs for different ML models
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Salary Predictor", 
        "🏋️ Weight Loss Estimator",
        "📚 Marks Predictor",
        "🏠 House Price Predictor"
    ])
    
    with tab1:
        try:
            from core.ml.sal_predictor.model import salary_predictor
            from babel.numbers import format_currency
            
            st.markdown("### 💰 Salary Predictor")
            st.markdown("Predict salary based on years of experience using machine learning.")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### Input")
                years = st.number_input(
                    "Years of Experience",
                    min_value=0,
                    max_value=50,
                    value=5,
                    step=1,
                    help="Enter the number of years of experience"
                )
                
                if st.button("Predict Salary"):
                    with st.spinner("Predicting..."):
                        try:
                            # Get prediction
                            predicted_salary = salary_predictor.predict_salary(years)
                            
                            # Format the salary with Indian Rupees
                            formatted_salary = format_currency(predicted_salary, 'INR', locale='en_IN')
                            
                            # Display the result
                            st.success(f"### Predicted Salary: {formatted_salary}")
                            
                            # Add some visual feedback
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            
            with col2:
                st.markdown("#### About")
                st.markdown("""
                This machine learning model predicts salary based on years of experience.
                
                **How to use:**
                1. Enter the number of years of experience
                2. Click 'Predict Salary'
                3. View the predicted salary in Indian Rupees (₹)
                
                *Note: This is a prediction based on the trained model and may not reflect actual salaries.*
                """)
                
        except ImportError as e:
            st.error(f"Failed to load ML module: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)
    
    with tab2:
        try:
            from core.ml.weight_loss_estimator.model import weight_loss_predictor
            
            st.markdown("### 🏋️ Weight Loss Estimator")
            st.markdown("Estimate your weight loss based on your fitness plan and lifestyle.")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.markdown("#### Your Details")
                
                # Input fields
                initial_weight = st.number_input(
                    "Current Weight (kg)",
                    min_value=30.0,
                    max_value=300.0,
                    value=70.0,
                    step=0.5,
                    help="Your current weight in kilograms"
                )
                
                goal_weight = st.number_input(
                    "Goal Weight (kg)",
                    min_value=30.0,
                    max_value=300.0,
                    value=65.0,
                    step=0.5,
                    help="Your target weight in kilograms"
                )
                
                exercise_minutes = st.slider(
                    "Daily Exercise (minutes)",
                    min_value=0,
                    max_value=240,
                    value=30,
                    step=5,
                    help="Average minutes of exercise per day"
                )
                
                calories = st.number_input(
                    "Daily Calorie Intake",
                    min_value=800,
                    max_value=5000,
                    value=2000,
                    step=50,
                    help="Your daily calorie consumption"
                )
                
                water = st.slider(
                    "Water Intake (liters)",
                    min_value=0.5,
                    max_value=10.0,
                    value=2.5,
                    step=0.5,
                    help="Liters of water consumed daily"
                )
                
                sleep_hours = st.slider(
                    "Sleep Hours",
                    min_value=4.0,
                    max_value=12.0,
                    value=7.5,
                    step=0.5,
                    help="Hours of sleep per night"
                )
                
                cheat_days = st.slider(
                    "Cheat Days (per month)",
                    min_value=0,
                    max_value=15,
                    value=2,
                    step=1,
                    help="Number of cheat days in a 30-day period"
                )
                
                if st.button("Estimate Weight Loss"):
                    with st.spinner("Calculating your weight loss estimate..."):
                        try:
                            # Prepare input data
                            input_data = {
                                'initial_weight': initial_weight,
                                'goal_weight': goal_weight,
                                'exercise_minutes': exercise_minutes,
                                'calories': calories,
                                'water': water,
                                'sleep_hours': sleep_hours,
                                'cheat_days': cheat_days
                            }
                            
                            # Get prediction
                            predicted_loss, months_needed = weight_loss_predictor.predict_weight_loss(input_data)
                            
                            # Display results
                            st.success(f"### Estimated Weight Loss: {predicted_loss:.2f} kg in 30 days")
                            
                            if months_needed is not None and months_needed > 0:
                                st.info(f"### 🎯 Time to reach goal: {months_needed:.1f} months")
                            
                            # Add some visual feedback
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            
            with col2:
                st.markdown("#### About This Model")
                st.markdown("""
                This machine learning model estimates weight loss based on various lifestyle factors.
                
                **How it works:**
                - The model uses a linear regression algorithm trained on fitness data
                - It considers multiple factors including exercise, diet, and sleep
                - Results are estimates based on statistical patterns
                
                **Tips for better results:**
                - Be honest with your input values
                - Track your actual progress and adjust as needed
                - Consult with a healthcare professional for personalized advice
                
                *Note: This is a prediction model and individual results may vary.*
                """)
                
                # Add some space
                st.markdown("---")
                
                # Add some health metrics
                st.markdown("#### Health Metrics")
                
                # Calculate BMI if we have height (simplified)
                if initial_weight > 0:
                    bmi = initial_weight / ((1.7) ** 2)  # Using average height for demonstration
                    st.metric("BMI (Estimate)", f"{bmi:.1f}")
                
                # Add some health tips based on input
                if calories < 1200:
                    st.warning("⚠️ Your calorie intake seems very low. Consider consulting a nutritionist.")
                
                if sleep_hours < 6:
                    st.warning("⚠️ Getting enough sleep is important for weight loss and overall health.")
                
                if water < 1.5:
                    st.warning("⚠️ Consider increasing your water intake for better health and metabolism.")
                
        except ImportError as e:
            st.error(f"Failed to load Weight Loss Estimator: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)
    
    with tab3:
        try:
            from core.ml.marks_predict.model import MarksPredictor
            
            st.markdown("### 📚 Marks Predictor")
            st.markdown("Predict your exam marks based on your daily study hours.")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.markdown("#### Study Details")
                
                # Input field for hours studied
                hours = st.number_input(
                    "Daily Study Hours",
                    min_value=0.5,
                    max_value=24.0,
                    value=3.0,
                    step=0.5,
                    help="Enter your average daily study hours"
                )
                
                if st.button("Predict Marks"):
                    with st.spinner("Predicting your marks..."):
                        try:
                            # Get prediction
                            predictor = MarksPredictor()
                            predicted_marks, recommendation = predictor.predict_marks(hours)
                            
                            # Display results with emoji based on performance
                            if predicted_marks < 40:
                                emoji = "❌"
                                color = "red"
                            elif predicted_marks < 70:
                                emoji = "⚠️"
                                color = "orange"
                            elif predicted_marks < 90:
                                emoji = "✅"
                                color = "green"
                            else:
                                emoji = "🎯"
                                color = "darkgreen"
                            
                            st.markdown(f"### {emoji} Predicted Marks: <span style='color:{color}'>{predicted_marks:.1f}/100</span>", 
                                      unsafe_allow_html=True)
                            
                            # Add a progress bar
                            st.progress(int(predicted_marks) / 100)
                            
                            # Show recommendation
                            st.markdown("#### 📝 Study Recommendation")
                            st.info(recommendation)
                            
                            # Add some visual feedback
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            
            with col2:
                st.markdown("#### About This Model")
                st.markdown("""
                This machine learning model predicts your exam marks based on your daily study hours.
                
                **How it works:**
                - The model uses linear regression trained on student performance data
                - It correlates study hours with academic performance
                - Results are estimates based on statistical patterns
                
                **Tips for better results:**
                - Be honest about your study hours
                - Focus on quality of study, not just quantity
                - Consider your learning style and adjust accordingly
                
                *Note: This is a predictive model and individual results may vary.*
                """)
                
                # Add some space
                st.markdown("---")
                
                # Add study tips
                st.markdown("#### 📊 Study Tips")
                
                tip = st.selectbox(
                    "Quick Study Tips:",
                    [
                        "Active Recall: Test yourself frequently",
                        "Spaced Repetition: Review material over time",
                        "Pomodoro Technique: 25 min focus, 5 min break",
                        "Teach Others: Explain concepts to a peer",
                        "Practice Problems: Apply what you learn"
                    ]
                )
                
        except ImportError as e:
            st.error(f"Failed to load Marks Predictor: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)

    with tab4:  # House Price Predictor tab
        try:
            from core.ml.houseprice.model import HousePricePredictor
            
            st.markdown("### 🏠 House Price Predictor")
            st.markdown("Estimate the price of a house based on its area and location.")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.markdown("#### Property Details")
                
                # Input field for area
                area = st.number_input(
                    "Area (sq ft)",
                    min_value=100.0,
                    max_value=10000.0,
                    value=1000.0,
                    step=50.0,
                    help="Enter the area of the property in square feet"
                )
                
                # Location type selector
                location_type = st.selectbox(
                    "Location Type",
                    ["Urban", "Suburban", "Rural"],
                    help="Select the type of location"
                )
                
                if st.button("Estimate Price"):
                    with st.spinner("Calculating price estimate..."):
                        try:
                            # Get prediction
                            predictor = HousePricePredictor()
                            predicted_price, price_per_sqft, location_multiplier = predictor.predict_price(
                                area, location_type.lower()
                            )
                            
                            # Get model parameters
                            params = predictor.get_model_parameters()
                            
                            # Display results
                            st.markdown("### 💰 Estimated Property Value")
                            st.markdown(f"#### ₹{predicted_price:,.2f}")
                            
                            # Show metrics
                            col1_metric, col2_metric = st.columns(2)
                            with col1_metric:
                                st.metric("Price per sq ft", f"₹{price_per_sqft:,.2f}")
                            with col2_metric:
                                st.metric("Location Multiplier", f"{location_multiplier:.1f}x")
                            
                            # Show model info in expander
                            with st.expander("📊 Model Details"):
                                st.markdown("#### Model Parameters")
                                st.markdown(f"- Base price: ₹{params['intercept']:,.2f}")
                                st.markdown(f"- Price per sq ft: ₹{params['coefficient']:,.2f}")
                                
                                st.markdown("#### Location Multipliers")
                                st.markdown("- Urban: 1.2x")
                                st.markdown("- Suburban: 1.0x")
                                st.markdown("- Rural: 0.8x")
                            
                            # Add some visual feedback
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            
            with col2:
                st.markdown("#### About This Model")
                st.markdown("""
                This machine learning model estimates house prices based on property area and location.
                
                **How it works:**
                - The model uses linear regression trained on real estate data
                - It considers both property size and location type
                - Location multipliers adjust the base price estimate
                
                **Features:**
                - Area-based pricing
                - Location-based adjustments
                - Detailed price breakdown
                - Transparent model parameters
                
                *Note: This is an estimate based on available data and may not reflect actual market prices.*
                """)
                
                # Add some space
                st.markdown("---")
                
                # Add price estimation guidelines
                st.markdown("#### 💡 Price Estimation Guidelines")
                
                st.markdown("""
                - **Small Apartment (500-800 sq ft):** 1-2 BHK
                - **Medium Apartment (800-1500 sq ft):** 2-3 BHK
                - **Large Apartment (1500-2500 sq ft):** 3-4 BHK
                - **Villa/Independent House (2500+ sq ft):** 4+ BHK
                
                *Prices vary based on location, amenities, and market conditions.*
                """)
            
        except ImportError as e:
            st.error(f"Failed to load House Price Predictor: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)
    
# JavaScript Tools Section
elif st.session_state.selected_tool == "JavaScript Tools":
    st.markdown("# 🛠️ JavaScript Tools")
    st.markdown("Launch interactive JavaScript applications and manage server-based tools.")
    
    # Tabs for different types of JavaScript tools
    tab1, tab2 = st.tabs(["📱 Web Apps", "🖥️ Server Tools"])
    
    with tab1:
        st.markdown("## 📱 Interactive Web Apps")
        st.markdown("Click to launch any of these interactive tools. A local HTTP server will be started if needed.")
        
        # Create 3 columns for better layout
        col1, col2, col3 = st.columns(3)
        
        # Static Projects - using a local HTTP server
        with col1:
            st.markdown("### 📧 Email Sender")
            if st.button("Open Email Sender", key="email_sender_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "email_sender")
                start_http_server(8001, project_dir)
                webbrowser.open_new_tab("http://localhost:8001/index2.html")
            
            st.markdown("### 📍 IP Tracker")
            if st.button("Open IP Tracker", key="ip_tracker_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "ip_tracker")
                start_http_server(8002, project_dir)
                webbrowser.open_new_tab("http://localhost:8002/index.html")
                
        with col2:
            st.markdown("### 🌐 Geolocation")
            if st.button("Open Geolocation", key="geolocation_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "geolocation")
                start_http_server(8003, project_dir)
                webbrowser.open_new_tab("http://localhost:8003/index.html")
            
            st.markdown("### 📸 Photo Capture")
            if st.button("Open Photo Capture", key="photo_capture_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "photo_capture")
                start_http_server(8004, project_dir)
                webbrowser.open_new_tab("http://localhost:8004/index.html")
                
        with col3:
            st.markdown("### 🎤 Speech to Text")
            if st.button("Open Speech to Text", key="speech_to_text_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "speech_to_text")
                start_http_server(8005, project_dir)
                webbrowser.open_new_tab("http://localhost:8005/index.html")
            
            st.markdown("### 🎥 Video Recorder")
            if st.button("Open Video Recorder", key="video_recorder_btn"):
                project_dir = os.path.join("core", "javascript_tools", "static_projects", "video_recorder")
                start_http_server(8006, project_dir)
                webbrowser.open_new_tab("http://localhost:8006/index.html")
    
    # Server Tools Tab
    with tab2:
        st.markdown("## 🖥️ Server-Based Tools")
        st.markdown("Manage server-based JavaScript applications. Make sure the respective servers are running.")
        
        # Create 3 columns for better layout
        col1, col2, col3 = st.columns(3)
        
        # Email Server Control Panel
        with col1:
            st.markdown("### 📧 Email Server")
            st.markdown("Full-featured email server with web interface")
            if st.button("Open Email Server Control Panel", key="btn_email_server"):
                st.session_state.selected_tool = "Email Server"
                st.session_state.server_type = 'email'
                st.rerun()
        
        # MailPicName Server
        with col2:
            st.markdown("### 📸 MailPicName")
            st.markdown("Image and name management server")
            if st.button("Open MailPicName Control Panel", key="btn_mailpicname"):
                st.session_state.selected_tool = "Email Server"
                st.session_state.server_type = 'mailpicname'
                st.rerun()
        
        # Video Email Server
        with col3:
            st.markdown("### 🎥 Video Email")
            st.markdown("Record and send video messages via email")
            if st.button("Open Video Email Control Panel", key="btn_video_email"):
                st.session_state.selected_tool = "Email Server"
                st.session_state.server_type = 'videoemail'
                st.rerun()
        
        st.markdown("---")
        st.info("💡 Server-based tools require a Node.js environment to be installed on your system.")

# 🧠 Burnout Recovery Assistant Section
elif st.session_state.selected_tool == "Burnout Assistant":
    try:
        from core.burnout_assistant import show_burnout_assistant
        show_burnout_assistant()
    except ImportError as e:
        st.error("Failed to load the Burnout Recovery Assistant. Please make sure all dependencies are installed.")
        st.code("pip install -r requirements.txt")
        st.exception(e)
    except Exception as e:
        st.error("An error occurred while loading the Burnout Recovery Assistant.")
        st.exception(e)
        
# 🤖 Agentic AI Assistant Section
elif st.session_state.selected_tool == "Agentic AI Assistant":
    try:
        from core.agentic_ai.streamlit_agentic_assistant import process_agentic_input
        
        # Set up the UI
        st.markdown("# 🤖 Agentic AI Assistant")
        st.markdown("""
        This is an agentic AI assistant that can interact with tools to perform tasks.
        
        **Available Tools:**
        - Project Scanner: Scans directories and summarizes README files
        
        **Example Queries:**
        - "Scan my project folder at 'path/to/folder' and summarize the README files"
        - "What's in the documentation for my project at 'path/to/project'?"
        """)
        
        # Initialize session state for chat history if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your agentic assistant. How can I help you today?"}
            ]
        
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input with unique key
        if prompt := st.chat_input("What would you like me to do?", key="main_chat_input"):
            process_agentic_input(prompt)
                    
    except ImportError as e:
        st.error("Failed to load the Agentic AI Assistant. Please make sure all dependencies are installed.")
        st.code("pip install -r core/agentic_ai/requirements.txt")
        st.exception(e)
    except Exception as e:
        st.error("An error occurred while loading the Agentic AI Assistant.")
        st.exception(e)

# 🔗 Quick Links Section
elif st.session_state.selected_tool == "Quick Links":
    st.markdown("# 🔗 Quick Links")
    st.markdown("Access your favorite external resources with a single click.")
    
    # Display the links panel
    show_links_panel()
    
# AWS Automation Section
elif st.session_state.selected_tool == "AWS Automation":
    st.markdown("# ☁️ AWS Automation")
    
    # Create tabs for different AWS services
    tab1, tab2, tab3 = st.tabs([
        "EC2 Management",
        "Lambda Management",
        "Coming Soon"  # Placeholder for future services
    ])
    
    with tab1:  # EC2 Management
        try:
            # Import AWS EC2 UI components
            from core.aws_automation.ec2_ui import show_ec2_dashboard
            
            # Show AWS EC2 Dashboard
            show_ec2_dashboard()
            
        except ImportError as e:
            st.error(f"Failed to load AWS EC2 Management: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)
        except Exception as e:
            st.error(f"An error occurred in AWS EC2 Management: {e}")
            st.exception(e)
    
    with tab2:  # Lambda Management
        try:
            from core.aws_automation.lambda_ui import show_lambda_dashboard
            show_lambda_dashboard()
        except ImportError as e:
            st.error(f"Failed to load Lambda Management: {e}")
            st.info("Please ensure all dependencies are installed from requirements.txt")
            st.exception(e)
    
    with tab3:  # Placeholder for future services
        st.markdown("## 🚧 More AWS Services Coming Soon")
        st.info("""
        We're working on adding more AWS services to help you manage your cloud resources.
        
        **Planned Features:**
        - S3 Bucket Management
        - RDS Database Management
        - CloudWatch Monitoring
        - IAM User/Role Management
        
        Stay tuned for updates!
        """)