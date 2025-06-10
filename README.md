# tra-receipt-scraper
🧾 Django REST API for scraping and extracting structured data from Tanzanian Revenue Authority (TRA) receipt verification URLs. Built with Selenium WebDriver for automated receipt processing and validation.

# 🧾 TRA Receipt Scraper API

A robust Django REST API service that automatically extracts structured data from Tanzanian Revenue Authority (TRA) receipt verification URLs. This service is designed to help businesses digitize and process their receipts for loyalty programs, accounting systems, and business analytics.

## 🚀 What it does

The Receipt Scraper API takes TRA receipt verification URLs (like `https://verify.tra.go.tz/xxxxx`) and returns structured JSON data containing:

- **Company Information**: Business name, TIN, VRN, tax office, contact details
- **Receipt Details**: Receipt number, date, time, verification codes
- **Customer Information**: Customer name, ID, mobile number (when available)
- **Purchased Items**: Detailed list of items with quantities and amounts
- **Financial Totals**: Tax calculations and total amounts
- **Verification Data**: Receipt validation codes and metadata

## 🛠 Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Web Scraping**: Selenium WebDriver with Chrome headless
- **HTML Parsing**: BeautifulSoup4
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Docker + DigitalOcean App Platform
- **Driver Management**: WebDriver Manager (automatic ChromeDriver handling)

## 🎯 Key Features

- ✅ **Reliable Scraping**: Retry logic
- ✅ **Production Ready**: Optimized for cloud deployment with Docker
- ✅ **Error Handling**: Comprehensive validation and error reporting
- ✅ **Health Monitoring**: Built-in health check endpoints
- ✅ **Auto-Validation**: Detects invalid receipts and provides meaningful errors
- ✅ **Performance Optimized**: Minimal browser resource usage
- ✅ **Scalable Architecture**: Ready for high-volume processing

## 🔧 API Endpoints

- `POST /api/scrape-receipt/` - Extract data from TRA receipt URL
- `GET /api/scrape-receipt/?url={receipt_url}` - Alternative GET method
- `GET /api/health/` - Health check and Chrome availability status

## 💼 Use Cases

- **Loyalty Programs**: Automatically process customer receipts for points calculation
- **Accounting Systems**: Digitize receipts for expense tracking and tax reporting
- **Business Analytics**: Extract sales data for reporting and insights
- **Receipt Verification**: Validate and authenticate TRA receipts
- **Data Integration**: Feed structured receipt data into existing business systems

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/receipt-scraper-project.git

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Test the API
curl -X POST http://localhost:8000/api/scrape-receipt/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://verify.tra.go.tz/your-receipt-url"}'
```

## 📋 Requirements

- Python 3.11+
- Chrome/Chromium browser
- ChromeDriver (automatically managed)
- Internet connection for TRA verification

## 🔒 Security & Compliance

- Headless browser operation for security
- No personal data storage (scrapes on-demand)

## 📊 Response Format

```json
{
  "company_info": {
    "name": "BUSINESS NAME LTD",
    "tin": "123456789",
    "vrn": "20-123456-A"
  },
  "receipt_info": {
    "receipt_no": "12345",
    "date": "2024-01-15",
    "time": "14:30:00"
  },
  "items": [
    {
      "description": "Product Name",
      "quantity": "2",
      "amount": "20000.00"
    }
  ],
  "totals": {
    "total_excl_tax": "18000.00",
    "total_tax": "2000.00",
    "total_incl_tax": "20000.00"
  }
}
```

---

Built for the Tanzanian business ecosystem to streamline receipt processing and enhance digital transformation initiatives.
