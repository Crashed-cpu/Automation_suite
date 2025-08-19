"""
External Links Module

This module provides functionality to display and manage external links
in the Automation Suite dashboard, such as portfolio, documentation, etc.
"""

# Define the links to be displayed in the dashboard
LINKS = {
    "Portfolio": {
        "url": "https://ayushautomates.netlify.app/",
        "icon": "🌐",
        "description": "View my portfolio and other projects"
    },
    "Bharat Electro": {
        "url": "https://bharatelectro.netlify.app/",
        "icon": "⚡",
        "description": "72 hours of legacy - My startup website"
    },
    "GitHub": {
        "url": "https://github.com/Crashed-cpu",
        "icon": "💻",
        "description": "Check out my GitHub profile and repositories"
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/the-ayush-factor/",
        "icon": "🔗",
        "description": "Connect with me on LinkedIn"
    }
}

def get_links():
    """
    Returns the dictionary of links to be displayed in the dashboard.
    
    Returns:
        dict: Dictionary containing link information
    """
    return LINKS

def add_link(name, url, icon="🔗", description=""):
    """
    Add a new link to be displayed in the dashboard.
    
    Args:
        name (str): Display name of the link
        url (str): URL to open when the link is clicked
        icon (str, optional): Emoji icon for the link. Defaults to "🔗".
        description (str, optional): Description of the link. Defaults to "".
    """
    LINKS[name] = {
        "url": url,
        "icon": icon,
        "description": description
    }

def remove_link(name):
    """
    Remove a link from the dashboard.
    
    Args:
        name (str): Name of the link to remove
    """
    if name in LINKS:
        del LINKS[name]
