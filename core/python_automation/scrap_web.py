"""
Web Scraping Module for Automation Suite

This module provides functionality to download and save website content,
including both static and dynamic content.
"""

import os
import time
from typing import Optional, Tuple, List, Dict, Any
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import streamlit as st

# Try to import selenium for dynamic content
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class WebScraper:
    """A class to handle web scraping operations."""
    
    def __init__(self, output_dir: str = "scraped_data"):
        """
        Initialize the WebScraper with an output directory.
        
        Args:
            output_dir (str): Directory to save scraped content (default: "scraped_data")
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.use_selenium = False
        
        if SELENIUM_AVAILABLE:
            self.setup_selenium()
    
    def setup_selenium(self):
        """Set up Selenium WebDriver for dynamic content."""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.use_selenium = True
        except Exception as e:
            st.warning(f"Selenium setup failed: {str(e)}. Falling back to static content only.")
            self.use_selenium = False
    
    def get_page_content(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the HTML content of a webpage.
        
        Args:
            url (str): URL of the webpage to scrape
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (page_content, final_url) or (None, error_message)
        """
        try:
            if self.use_selenium and self._is_dynamic(url):
                self.driver.get(url)
                time.sleep(3)  # Wait for dynamic content to load
                return self.driver.page_source, self.driver.current_url
            else:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text, response.url
        except Exception as e:
            return None, f"Error fetching {url}: {str(e)}"
    
    def _is_dynamic(self, url: str) -> bool:
        """Check if a URL likely contains dynamic content."""
        # Simple heuristic: check for common SPA frameworks or specific extensions
        dynamic_indicators = [
            'react', 'vue', 'angular', '.aspx', '.php',
            '#!/', '#!', '_escaped_fragment_='
        ]
        return any(indicator in url.lower() for indicator in dynamic_indicators)
    
    def extract_links(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """
        Extract all links from an HTML page.
        
        Args:
            html (str): HTML content of the page
            base_url (str): Base URL for resolving relative URLs
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'url' and 'text' keys
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            url = a_tag['href']
            if not url.startswith(('http://', 'https://')):
                url = urljoin(base_url, url)
            links.append({
                'url': url,
                'text': a_tag.get_text(strip=True) or url
            })
        
        return links
    
    def extract_images(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """
        Extract all images from an HTML page.
        
        Args:
            html (str): HTML content of the page
            base_url (str): Base URL for resolving relative URLs
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'url' and 'alt' keys
        """
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        
        for img in soup.find_all('img', src=True):
            src = img['src']
            if not src.startswith(('http://', 'https://')):
                src = urljoin(base_url, src)
            images.append({
                'url': src,
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        return images
    
    def save_content(self, content: Any, filename: str, subfolder: str = '') -> str:
        """
        Save content to a file in the output directory.
        
        Args:
            content: Content to save (text, dict, list, etc.)
            filename (str): Name of the file to save
            subfolder (str): Optional subfolder within the output directory
            
        Returns:
            str: Path to the saved file
        """
        folder = self.output_dir / subfolder
        folder.mkdir(parents=True, exist_ok=True)
        
        if filename.endswith('.json') and isinstance(content, (dict, list)):
            filepath = folder / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            if not isinstance(content, str):
                content = str(content)
            filepath = folder / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return str(filepath)
    
    def scrape_website(self, url: str, max_pages: int = 10) -> Dict[str, Any]:
        """
        Scrape a website and save its content.
        
        Args:
            url (str): URL of the website to scrape
            max_pages (int): Maximum number of pages to scrape (default: 10)
            
        Returns:
            Dict[str, Any]: Dictionary with scraping results and statistics
        """
        start_time = time.time()
        results = {
            'url': url,
            'success': False,
            'pages_scraped': 0,
            'total_links': 0,
            'total_images': 0,
            'saved_files': [],
            'error': None
        }
        
        try:
            # Scrape the main page
            html, final_url = self.get_page_content(url)
            if not html:
                results['error'] = f"Failed to fetch {url}: {final_url}"
                return results
            
            # Save the main page
            domain = urlparse(final_url).netloc
            timestamp = int(time.time())
            main_page_path = self.save_content(html, f"{domain}_{timestamp}.html", 'pages')
            results['saved_files'].append(main_page_path)
            results['pages_scraped'] += 1
            
            # Extract and save links
            links = self.extract_links(html, final_url)
            results['total_links'] = len(links)
            if links:
                links_path = self.save_content(links, f"{domain}_links_{timestamp}.json", 'data')
                results['saved_files'].append(links_path)
            
            # Extract and save images
            images = self.extract_images(html, final_url)
            results['total_images'] = len(images)
            if images:
                images_path = self.save_content(images, f"{domain}_images_{timestamp}.json", 'data')
                results['saved_files'].append(images_path)
            
            # Scrape additional pages (up to max_pages)
            for i, link in enumerate(links[:max_pages-1]):
                try:
                    page_html, page_url = self.get_page_content(link['url'])
                    if page_html:
                        page_filename = f"{urlparse(page_url).netloc}_{i+2}_{timestamp}.html"
                        page_path = self.save_content(page_html, page_filename, 'pages')
                        results['saved_files'].append(page_path)
                        results['pages_scraped'] += 1
                except Exception as e:
                    st.warning(f"Error scraping {link['url']}: {str(e)}")
            
            results['success'] = True
            results['time_elapsed'] = time.time() - start_time
            
        except Exception as e:
            results['error'] = str(e)
        
        # Save the results
        results_path = self.save_content(
            results, 
            f"{domain}_scraping_results_{timestamp}.json",
            'reports'
        )
        results['report_path'] = results_path
        
        return results

def scrape_website_ui():
    """Streamlit UI for the web scraping functionality."""
    st.markdown("## 🌐 Web Scraper")
    
    url = st.text_input("Enter website URL to scrape:", "https://")
    max_pages = st.slider("Maximum pages to scrape:", 1, 50, 5)
    
    if st.button("Start Scraping"):
        if not url.startswith(('http://', 'https://')):
            st.error("Please enter a valid URL starting with http:// or https://")
            return
        
        with st.spinner("Scraping website. This may take a while..."):
            scraper = WebScraper()
            results = scraper.scrape_website(url, max_pages)
            
            if results['success']:
                st.success(f"Successfully scraped {results['pages_scraped']} pages!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Links Found", results['total_links'])
                with col2:
                    st.metric("Total Images Found", results['total_images'])
                
                st.markdown("### Saved Files")
                for file_path in results['saved_files']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.code(file_path, language='text')
                    
                    if file_path.endswith('.html'):
                        with col2:
                            # Create a button that will open the HTML in a new tab
                            with open(file_path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            
                            # Create a unique key for this file's button
                            btn_key = f"view_html_{os.path.basename(file_path).replace('.', '_')}"
                            
                            # Create a proper HTML document with base URL
                            html_with_base = f"""
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <meta charset="UTF-8">
                                <title>Preview</title>
                                <base href="http://{urlparse(results['url']).netloc}" target="_blank">
                                <style>
                                    body {{ 
                                        font-family: Arial, sans-serif; 
                                        padding: 20px; 
                                        max-width: 1200px; 
                                        margin: 0 auto;
                                    }}
                                </style>
                            </head>
                            <body>
                                {html_content}
                            </body>
                            </html>
                            """
                            
                            # Encode the HTML content for the data URL
                            import base64
                            import urllib.parse
                            encoded_html = base64.b64encode(html_with_base.encode('utf-8')).decode('utf-8')
                            data_url = f"data:text/html;base64,{encoded_html}"
                            
                            # Create a button that opens the HTML in a new tab
                            button_html = f"""
                            <a href="{data_url}" target="_blank" style="text-decoration: none;">
                                <button style="
                                    background-color: #4CAF50;
                                    color: white;
                                    border: none;
                                    padding: 0.5rem 1rem;
                                    border-radius: 4px;
                                    cursor: pointer;
                                    width: 100%;
                                    font-size: 0.9rem;
                                ">
                                    👁️ View HTML
                                </button>
                            </a>
                            """
                            st.markdown(button_html, unsafe_allow_html=True)
                            
                            # Add download button next to view button
                            st.download_button(
                                label="⬇️ Download",
                                data=html_content,
                                file_name=os.path.basename(file_path),
                                mime="text/html",
                                key=f"dl_{os.path.basename(file_path)}",
                                use_container_width=True
                            )
                    
                    st.markdown("---")  # Add a separator between files
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download All Files",
                        data=json.dumps(results, indent=2),
                        file_name=f"scraping_results_{int(time.time())}.json",
                        mime="application/json"
                    )
            else:
                st.error(f"Scraping failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    # For testing the module directly
    import streamlit as st
    st.title("🌐 Web Scraper")
    scrape_website_ui()