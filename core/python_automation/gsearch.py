"""
Google Search Module for Automation Suite

This module provides functionality to perform Google searches and return results
in a format suitable for the Streamlit dashboard.
"""

from googlesearch import search
from typing import List, Dict
import streamlit as st
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Data class to store search result information."""
    title: str
    url: str
    description: str = ""

def google_search(query: str, num_results: int = 5) -> List[SearchResult]:
    """
    Perform a Google search and return results.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (default: 5)
        
    Returns:
        List[SearchResult]: List of search results
    """
    try:
        # Perform the search
        search_results = search(query, num_results=num_results, advanced=True)
        
        # Convert to our SearchResult objects
        results = []
        for result in search_results:
            results.append(SearchResult(
                title=result.title,
                url=result.url,
                description=result.description
            ))
        
        return results
        
    except Exception as e:
        st.error(f"Error performing search: {str(e)}")
        return []

def display_search_results(results: List[SearchResult]):
    """
    Display search results in Streamlit format.
    
    Args:
        results (List[SearchResult]): List of search results to display
    """
    if not results:
        st.warning("No search results found.")
        return
    
    for i, result in enumerate(results, 1):
        with st.container():
            st.subheader(f"{i}. {result.title}")
            st.caption(result.url)
            st.write(result.description)
            st.markdown("---")

def search_ui():
    """
    Streamlit UI component for the search functionality.
    """
    st.markdown("## 🔍 Google Search")
    
    # Search input
    query = st.text_input("Search Google", "")
    
    # Number of results selector
    num_results = st.slider("Number of results", 1, 10, 5)
    
    if query:
        with st.spinner(f"Searching for '{query}'..."):
            results = google_search(query, num_results)
            display_search_results(results)

if __name__ == "__main__":
    # For testing the module directly
    import streamlit as st
    st.title("🔍 Google Search Test")
    search_ui()