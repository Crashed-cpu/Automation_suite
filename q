warning: in the working copy of 'app.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/app.py b/app.py[m
[1mindex 38f6c53..486cf3d 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -1,9 +1,10 @@[m
 import os[m
 import streamlit as st[m
 from core.linux_tools import bash_runner[m
[31m-from core.ui.email_server_ui import show_email_server_page[m
 from core.docker_automation import docker_runner[m
[31m-from core.others.ui import show_links_panel[m
[32m+[m[32mfrom core.burnout_assistant import show_burnout_assistant[m
[32m+[m[32mfrom core.agentic_ai.streamlit_agentic_assistant import show_agentic_assistant[m
[32m+[m[32mfrom core.ui.email_server_ui import show_email_server_page[m
 [m
 # ⚙️ Initial Config[m
 st.set_page_config([m
[36m@@ -80,12 +81,16 @@[m [mwith st.sidebar:[m
     if st.button("🐳 Docker Automation", key="btn_docker"):[m
         st.session_state.selected_tool = "Docker Automation"[m
         st.session_state.selected_command = None[m
[31m-        [m
[32m+[m
[32m+[m[32m    if st.button("🤖 AI Assistants", key="btn_ai"):[m
[32m+[m[32m        st.session_state.selected_tool = "AI Assistants"[m
[32m+[m[32m        st.session_state.selected_command = None[m
[32m+[m
     if st.button("🐍 Python Automation", key="btn_python"):[m
         st.session_state.selected_tool = "Python Automation"[m
         st.session_state.selected_command = None[m
         [m
[31m-    if st.button("🤖 ML Models", key="btn_ml"):[m
[32m+[m[32m    if st.button("📊 ML Models", key="btn_ml"):[m
         st.session_state.selected_tool = "ML Models"[m
         st.session_state.selected_command = None[m
 [m
[36m@@ -223,6 +228,7 @@[m [melif st.session_state.selected_tool == "Docker Automation":[m
                     else:[m
                         st.error("❌ No output or command failed.")[m
 [m
[32m+[m
 # 🐍 Python Automation Module[m
 elif st.session_state.selected_tool == "Python Automation":[m
     st.markdown("## 🐍 Python Automation")[m
[36m@@ -230,8 +236,8 @@[m [melif st.session_state.selected_tool == "Python Automation":[m
     # Create tabs for different Python automation features[m
     tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([[m
         "🔔 Notifications",[m
[31m-        "🌐 Web Scraper",[m
         "🔍 Google Search",[m
[32m+[m[32m        "🌐 Web Scraper",[m
         "📧 Email Sender",[m
         "🎨 Image Generator",[m
         "🎭 Face Swap",[m
[36m@@ -880,89 +886,99 @@[m [melif st.session_state.selected_tool == "JavaScript Tools":[m
     st.markdown("Launch interactive JavaScript applications and manage server-based tools.")[m
     [m
     # Tabs for different types of JavaScript tools[m
[31m-    tab1, tab2 = st.tabs(["📁 Static Apps", "🛠️ Server Tools"])[m
[32m+[m[32m    tab1, tab2 = st.tabs(["📱 Web Apps", "🖥️ Server Tools"])[m
     [m
     with tab1:[m
[31m-        st.markdown("## 🚀 Launch JavaScript Applications")[m
[31m-        st.markdown("Click the buttons below to launch interactive JavaScript applications in new tabs.")[m
[32m+[m[32m        st.markdown("## 📱 Interactive Web Apps")[m
[32m+[m[32m        st.markdown("Click to launch any of these interactive tools in a new tab.")[m
         [m
[31m-        # Get the absolute path to the static projects directory[m
[31m-        base_path = os.path.abspath("core/javascript_tools/static_projects")[m
[32m+[m[32m        # Create 3 columns for better layout[m
[32m+[m[32m        col1, col2, col3 = st.columns(3)[m
         [m
[31m-        # List of available JavaScript tools[m
[31m-        js_tools = [[m
[31m-            {[m
[31m-                "name": "✉️ Email Sender",[m
[31m-                "path": os.path.join("email_sender", "index2.html"),[m
[31m-                "description": "Send emails with custom templates"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "📡 IP Tracker",[m
[31m-                "path": os.path.join("ip_tracker", "index.html"),[m
[31m-                "description": "Track and locate IP addresses on a map"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "📍 Geolocation",[m
[31m-                "path": os.path.join("geolocation", "index.html"),[m
[31m-                "description": "Get your current location and show on map"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "📸 Photo Capture",[m
[31m-                "path": os.path.join("photo_capture", "index.html"),[m
[31m-                "description": "Capture photos using your webcam"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "🛍️ Product Tracker",[m
[31m-                "path": os.path.join("product_tracker", "public", "index.html"),[m
[31m-                "description": "Track product prices and availability"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "🎤 Speech to Text",[m
[31m-                "path": os.path.join("speech_to_text", "index.html"),[m
[31m-                "description": "Convert speech to text in real-time"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "🎥 Video Recorder",[m
[31m-                "path": os.path.join("video_recorder", "index.html"),[m
[31m-                "description": "Record videos using your webcam"[m
[31m-            },[m
[31m-            {[m
[31m-                "name": "💬 WhatsApp Integration",[m
[31m-                "path": os.path.join("whatsapp_integration", "index.html"),[m
[31m-                "description": "Send WhatsApp messages programmatically"[m
[31m-            }[m
[31m-        ][m
[32m+[m[32m        # Static Projects[m
[32m+[m[32m        with col1:[m
[32m+[m[32m            if st.button("📧 Email Sender"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/email_sender/index2.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Email Sender</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m            if st.button("📍 IP Tracker"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/ip_tracker/index.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open IP Tracker</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m        with col2:[m
[32m+[m[32m            if st.button("🌐 Geolocation"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/geolocation/index.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Geolocation</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m            if st.button("📸 Photo Capture"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/photo_capture/index.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Photo Capture</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m        with col3:[m
[32m+[m[32m            if st.button("🎤 Speech to Text"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/speech_to_text/index.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Speech to Text</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m            if st.button("🎥 Video Recorder"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="/static/video_recorder/index.html" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Video Recorder</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m    with tab2:[m
[32m+[m[32m        st.markdown("## 🖥️ Server-Based Tools")[m
[32m+[m[32m        st.markdown("Manage server-based JavaScript applications.")[m
         [m
[31m-        # Display tools in a grid[m
[31m-        cols = st.columns(2)[m
[31m-        for i, tool in enumerate(js_tools):[m
[31m-            with cols[i % 2]:[m
[31m-                with st.container():[m
[31m-                    st.markdown(f"### {tool['name']}")[m
[31m-                    st.caption(tool['description'])[m
[31m-                    [m
[31m-                    # Create the full file path[m
[31m-                    full_path = os.path.join(base_path, tool['path'])[m
[31m-                    [m
[31m-                    # Create a button that opens the tool in the default browser[m
[31m-                    if st.button(f"🚀 Launch {tool['name'].split()[-1]}", [m
[31m-                            key=f"js_tool_{i}",[m
[31m-                            help=f"Open {tool['name']} in your default browser"):[m
[31m-                        try:[m
[31m-                            # Convert Windows path to file URL[m
[31m-                            file_url = 'file:///' + full_path.replace('\\', '/').replace(' ', '%20')[m
[31m-                            import webbrowser[m
[31m-                            webbrowser.open_new_tab(file_url)[m
[31m-                            st.success(f"Opening {tool['name']} in your default browser...")[m
[31m-                        except Exception as e:[m
[31m-                            st.error(f"Failed to open {tool['name']}: {str(e)}")[m
[31m-                            st.info(f"You can manually open: {full_path}")[m
[31m-                    [m
[31m-                    # Show the file path for debugging[m
[31m-                    with st.expander("File Location"):[m
[31m-                        st.code(full_path, language="text")[m
[31m-                    [m
[31m-                    st.markdown("---")[m
[32m+[m[32m        # Create 3 columns for better layout[m
[32m+[m[32m        col1, col2, col3 = st.columns(3)[m
[32m+[m[41m        [m
[32m+[m[32m        # Server Projects[m
[32m+[m[32m        with col1:[m
[32m+[m[32m            if st.button("📧 Email Server"):[m
[32m+[m[32m                st.session_state.selected_tool = "Email Server"[m
[32m+[m[32m                st.experimental_rerun()[m
[32m+[m[41m                [m
[32m+[m[32m        with col2:[m
[32m+[m[32m            if st.button("📸 MailPicName"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="http://localhost:3000" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open MailPicName</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m        with col3:[m
[32m+[m[32m            if st.button("🎥 Video Email"):[m
[32m+[m[32m                st.markdown("""[m
[32m+[m[32m                <a href="http://localhost:4000" target="_blank">[m
[32m+[m[32m                    <button style="width:100%;">Open Video Email</button>[m
[32m+[m[32m                </a>[m
[32m+[m[32m                """, unsafe_allow_html=True)[m
[32m+[m[41m                [m
[32m+[m[32m                # This section appears to be leftover from a previous implementation[m
[32m+[m[32m                # and is not needed for the current video email functionality[m
[32m+[m[32m                pass[m
[32m+[m[41m                [m
[32m+[m[32m                # Show the file path for debugging[m
[32m+[m[32m                with st.expander("File Location"):[m
[32m+[m[32m                    st.code("http://localhost:4000", language="text")[m
[32m+[m[41m                [m
[32m+[m[32m                st.markdown("---")[m
         [m
     with tab2:[m
         st.markdown("## 🖥️ Server-Based Tools")[m
