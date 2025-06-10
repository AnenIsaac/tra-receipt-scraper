"""
Receipt scraper utility for extracting data from TRA receipts.
Optimized version that minimizes ChromeDriver usage time.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import re
import logging
import time

logger = logging.getLogger(__name__)

def get_html_content(url, max_retries=3, wait_time=1):
    """
    Fetch HTML content from a URL using ChromeDriver
    
    Args:
        url (str): The URL to fetch
        max_retries (int): Maximum number of retry attempts
        wait_time (int): Time to wait for page load in seconds
        
    Returns:
        str: HTML content of the page
    """
    # Set up Selenium WebDriver in headless mode with performance optimizations
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    
    for attempt in range(max_retries):
        try:
            # Use system-installed ChromeDriver
            service = Service('/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            
            # Load the page
            driver.get(url)
            
            # Wait minimal time for the page to load
            time.sleep(wait_time)
            
            # Get the page source
            html_content = driver.page_source
            
            # Close the browser immediately
            driver.quit()
            
            return html_content
            
        except WebDriverException as e:
            if attempt < max_retries - 1:
                logger.warning(f"WebDriver error on attempt {attempt + 1}: {e}. Retrying...")
                time.sleep(1)  # Short delay before retry
            else:
                logger.error(f"WebDriver error after {max_retries} attempts: {e}")
                raise Exception(f"Failed to scrape receipt: {e}")
        except Exception as e:
            logger.error(f"Error fetching HTML: {e}")
            raise Exception(f"Failed to fetch HTML content: {e}")
        finally:
            # Make sure driver is closed even if an exception occurs
            if 'driver' in locals():
                driver.quit()

def parse_receipt_data(html_content, url):
    """
    Parse the HTML content to extract receipt data
    
    Args:
        html_content (str): The HTML content to parse
        url (str): The source URL for reference
        
    Returns:
        dict: The structured receipt data
    """
    receipt_data = {
        "company_info": {},
        "customer_info": {},
        "receipt_info": {},
        "items": [],
        "totals": {},
        "verification": {}
    }
    
    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract company information
        company_section = soup.find('div', class_='invoice-info')
        if company_section:
            # Company name
            company_name = soup.find('h4', text=lambda t: t and 'COTY COMPANY LIMITED' in t)
            if company_name:
                receipt_data["company_info"]["name"] = company_name.text.strip()
            
            invoice_col = company_section.find('div', class_='invoice-col')
            if invoice_col:
                text = invoice_col.get_text()
                
                # Use a dictionary to map regex patterns to fields for cleaner code
                patterns = {
                    "po_box": r'P\.O BOX ([0-9]+)',
                    "mobile": r'MOBILE:\s*(\d+)',
                    "tin": r'TIN:\s*(\d+)',
                    "vrn": r'VRN:\s*(\w+)',
                    "serial_no": r'SERIAL NO:\s*(\w+)',
                    "uin": r'UIN:\s*(\S+)',
                    "tax_office": r'TAX OFFICE:\s*(.*?)(?=\n|$)'
                }
                
                # Extract fields based on patterns
                for field, pattern in patterns.items():
                    match = re.search(pattern, text)
                    if match:
                        receipt_data["company_info"][field] = match.group(1).strip()
        
        # Extract customer information and receipt info
        invoice_headers = soup.find_all('div', class_='col-xs-12 invoice-header')
        for header in invoice_headers:
            text = header.get_text()
            
            # Customer info section
            if 'CUSTOMER NAME:' in text:
                patterns = {
                    "name": r'CUSTOMER NAME:\s*(.*?)(?=\n|$)',
                    "id_type": r'CUSTOMER ID TYPE:\s*(.*?)(?=\n|$)',
                    "id": r'CUSTOMER ID:\s*(.*?)(?=\n|$)',
                    "mobile": r'CUSTOMER MOBILE:\s*(.*?)(?=\n|$)'
                }
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, text)
                    if match:
                        receipt_data["customer_info"][field] = match.group(1).strip()
            
            # Receipt info section
            elif 'RECEIPT NO:' in text:
                patterns = {
                    "receipt_no": r'RECEIPT NO:\s*(.*?)(?=\n|$)',
                    "z_number": r'Z NUMBER:\s*(.*?)(?=\n|$)',
                    "date": r'RECEIPT DATE:\s*(.*?)(?=\n|$)',
                    "time": r'RECEIPT TIME:\s*(.*?)(?=\n|$)'
                }
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, text)
                    if match:
                        receipt_data["receipt_info"][field] = match.group(1).strip()
            
            # Verification code section
            elif 'RECEIPT VERIFICATION CODE' in text:
                verification_code = re.search(r'([A-Z0-9]+)(?=\s*<|$)', header.get_text())
                if verification_code:
                    receipt_data["verification"]["code"] = verification_code.group(1).strip()
        
        # Extract items
        items_table = soup.find('table', class_='table-striped')
        if items_table:
            rows = items_table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    item = {
                        "description": cols[0].text.strip(),
                        "quantity": cols[1].text.strip(),
                        "amount": cols[2].text.strip()
                    }
                    receipt_data["items"].append(item)
        
        # Extract totals
        totals_table = soup.find_all('table', class_='table')[-1]  # Get the last table which has the totals
        if totals_table:
            rows = totals_table.find_all('tr')
            for row in rows:
                header = row.find('th')
                value = row.find('td')
                if header and value:
                    key = header.text.strip().lower().replace(' ', '_').replace(':', '')
                    receipt_data["totals"][key] = value.text.strip()
        
        # Add source URL
        receipt_data["source_url"] = url
        
        return receipt_data
        
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise Exception(f"Failed to process receipt data: {e}")

def scrape_receipt_data(url):
    """
    Scrape receipt data from the provided URL
    
    Args:
        url (str): The URL of the receipt to scrape
        
    Returns:
        dict: The structured receipt data
    """
    try:
        # Step 1: Get the HTML content (browser opens and closes quickly)
        html_content = get_html_content(url)
        
        # Step 2: Parse the HTML content (browser is already closed)
        receipt_data = parse_receipt_data(html_content, url)
        
        return receipt_data
        
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        raise Exception(f"Failed to scrape receipt: {e}")