import streamlit as st
from core.javascript_tools.server_manager import servers, email_server, mailpicname_server, videoemail_server

def show_server_control_panel(server, server_name):
    """Display a server control panel for the given server instance."""
    st.markdown(f"# 📧 {server_name}")
    st.markdown(f"Manage the {server_name} server.")
    
    # Add a refresh button at the top
    if st.button("🔄 Refresh Status", key=f"refresh_{server_name.lower().replace(' ', '_')}"):
        st.rerun()
    
    # Check server status with error handling
    try:
        is_running, pid = server.is_running()
        status_error = None
    except Exception as e:
        is_running = False
        status_error = str(e)
        st.error(f"Error checking server status: {status_error}")
    
    # Status and control columns
    col1, col2, col3 = st.columns([1, 1, 2])
    
    # Display status with more details
    with col1:
        if is_running:
            st.success("🟢 Server is running")
            st.caption(f"PID: {pid or 'N/A'}")
        else:
            st.warning("🔴 Server is stopped")
            if status_error:
                st.error(f"Error: {status_error}")
    
    with col2:
        if is_running:
            if st.button("🛑 Stop Server", type="primary", key=f"stop_{server_name.lower().replace(' ', '_')}"):
                with st.spinner("Stopping server..."):
                    success, message = server.stop_server()
                    if success:
                        st.success(message)
                    else:
                        st.error(f"Failed to stop server: {message}")
                    st.rerun()
        else:
            if st.button("🚀 Start Server", type="primary", key=f"start_{server_name.lower().replace(' ', '_')}"):
                with st.spinner("Starting server..."):
                    success, message = server.start_server()
                    if success:
                        st.success(message)
                    else:
                        st.error(f"Failed to start server: {message}")
                    st.rerun()
    
    with col3:
        if is_running:
            if st.button("🌐 Open Web Interface", key=f"open_web_ui_{server_name.lower().replace(' ', '_')}"):
                import webbrowser
                webbrowser.open_new_tab(f"http://localhost:{server.port}")
            st.caption(f"Port: {server.port}")
    
    # Server information columns
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("### Server Information")
        
        info_data = [
            ("Status", "🟢 Running" if is_running else "🔴 Stopped"),
            ("Port", str(server.port)),
            ("Process ID", str(pid) if pid else "N/A"),
            ("Web Interface", f"http://localhost:{server.port}"),
            ("Server Directory", str(server.server_dir))
        ]
        
        for label, value in info_data:
            st.markdown(f"**{label}:** {value}")
        
        # Show last log entry if available
        logs = server.get_logs(1)
        if logs:
            with st.expander("📝 Last Log Entry"):
                st.code(logs[0], language="text")
    
    with info_col2:
        st.markdown("### Quick Actions")
        if st.button("📋 Copy .env Template", key=f"copy_env_{server_name.lower()}"):
            env_template = """# Gmail SMTP Configuration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
SENDER_NAME=\"Your Name\"
PORT=3001
FRONTEND_URL=http://localhost:3001"""
            st.code(env_template, language="bash")
            st.toast("📋 .env template copied to clipboard!")
    
    # Server logs
    st.markdown("### Server Logs")
    logs = server.get_logs(20)
    if logs:
        log_container = st.container(height=300)
        with log_container:
            for log in logs:
                st.code(log, language="text")
    else:
        st.info("No logs available. Start the server to see logs.")
    
    # Documentation
    with st.expander("📖 Documentation & Troubleshooting"):
        st.markdown("""
        ### Email Server Setup Guide
        
        1. **Gmail Account Setup**
           - Enable 2-factor authentication on your Google Account
           - Generate an App Password for this application
           - Use the App Password as `GMAIL_APP_PASSWORD`
        
        2. **.env Configuration**
           - Place the `.env` file in the server directory
           - Required variables:
             ```
             GMAIL_USER=your-email@gmail.com
             GMAIL_APP_PASSWORD=your-app-password
             SENDER_NAME=\"Your Name\"
             PORT=3001
             FRONTEND_URL=http://localhost:3001
             ```
        
        3. **Common Issues**
           - Make sure port 3001 is not in use by another application
           - Check that your Gmail account has "Less secure app access" enabled
           - Verify your App Password has the correct permissions
           - Ensure your firewall allows connections to port 3001
        
        ### Troubleshooting
        - **Server won't start:** Check if port 3001 is already in use
        - **Authentication failed:** Verify your Gmail App Password
        - **Connection refused:** Ensure the server is running before accessing the web interface
        """)


def show_email_server_page(server_type=None):
    """Display the server management dashboard.
    
    Args:
        server_type (str, optional): The type of server to show by default. 
            One of: 'email', 'mailpicname', 'videoemail', or None to keep current selection.
    """
    # Get the server type from session state if not provided
    if server_type is None:
        server_type = st.session_state.get('server_type', 'email')
    
    # Set the default tab based on server_type
    if server_type == 'email':
        default_tab = 0
    elif server_type == 'mailpicname':
        default_tab = 1
    elif server_type == 'videoemail':
        default_tab = 2
    else:
        default_tab = 0  # Default to first tab if invalid type
    
    st.markdown("# 🖥️ Server Management")
    st.markdown("Manage your server applications.")
    
    # Create tabs for each server
    tabs = st.tabs(["📧 Email Server", "📸 MailPicName", "🎥 Video Email"])
    
    with tabs[0]:
        show_server_control_panel(email_server, "Email Server")
        
    with tabs[1]:
        show_server_control_panel(mailpicname_server, "MailPicName")
        
    with tabs[2]:
        show_server_control_panel(videoemail_server, "Video Email")
