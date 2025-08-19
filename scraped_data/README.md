# Scraped Data

This directory stores data collected by the web scraping module.

## 📂 Directory Structure

- `raw_html/`: Raw HTML content from scraped pages
- `data/`: Processed and structured data
- `pages/`: Complete web pages (HTML + assets)
- `reports/`: Generated reports and analysis

## 📝 Usage

### For Web Scraping
1. Run the web scraper from the dashboard
2. View results in the respective subdirectories
3. Access processed data through the application interface

### File Naming
- Files are automatically named using the URL hash and timestamp
- Example: `example_com_abc123_20230809.html`

## 🔒 Data Retention

- Old files are not automatically cleaned up
- Manually remove files when no longer needed
- Be mindful of storage usage with large scrapes

## ⚠️ Legal Notice

- Respect website terms of service
- Check robots.txt before scraping
- Implement appropriate delays between requests
- Consider caching to avoid unnecessary re-scraping
