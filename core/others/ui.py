"""
External Links UI Module

This module provides the Streamlit UI components for displaying external links
in the Automation Suite dashboard.
"""
import streamlit as st
import webbrowser
from typing import Dict, Any

def show_links_panel():
    """
    Displays a panel with clickable buttons for external links.
    """
    from ..others import get_links
    
    # Get the links from the configuration
    links = get_links()
    
    if not links:
        st.info("No external links configured.")
        return
    
    # Create columns for the buttons (2 columns per row)
    cols = st.columns(2)
    
    for idx, (name, link_info) in enumerate(links.items()):
        with cols[idx % 2]:
            display_link_button(name, link_info)

def display_link_button(name: str, link_info: Dict[str, Any]):
    """
    Displays a styled button for a single link.
    
    Args:
        name (str): Display name of the link
        link_info (dict): Dictionary containing 'url', 'icon', and 'description'
    """
    # Create a button with the link's icon and name
    button_label = f"{link_info.get('icon', '🔗')} {name}"
    
    # Use a container for better styling
    with st.container():
        # Button to open the link
        if st.button(
            button_label,
            key=f"link_btn_{name}",
            help=link_info.get('description', ''),
            use_container_width=True
        ):
            # Open the URL in a new tab
            webbrowser.open_new_tab(link_info['url'])
        
        # Optional: Add a small description below the button
        if 'description' in link_info and link_info['description']:
            st.caption(link_info['description'], help=link_info['description'])
        
        # Add some spacing between buttons
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

def add_link_ui():
    """
    Provides a UI for adding new links to the dashboard.
    For admin/configuration purposes.
    """
    from ..others import add_link
    
    st.markdown("### Add New Link")
    
    with st.form("add_link_form"):
        name = st.text_input("Link Name", "")
        url = st.text_input("URL", "https://")
        icon = st.text_input("Icon (emoji)", "🔗")
        description = st.text_area("Description", "")
        
        submitted = st.form_submit_button("Add Link")
        
        if submitted:
            if name and url:
                add_link(name, url, icon, description)
                st.success(f"Link '{name}' added successfully!")
            else:
                st.error("Please provide both a name and URL for the link.")
