# 🗺️ Google Maps Restaurant Scraper - Complete Data Extraction Tool

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

A powerful, enterprise-grade Python web scraper that extracts **comprehensive restaurant data** from Google Maps search results. Unlike basic scrapers, this tool performs **two-stage scraping**: first collecting restaurant listings, then diving deep into each restaurant's individual page to extract 20+ data points including contact information, service options, reviews, and more.

Perfect for market research, business intelligence, competitive analysis, and building restaurant databases.

## ✨ Key Features

### 🎯 Two-Stage Scraping System
- **Stage 1**: Scrolls through search results and collects all restaurant URLs
- **Stage 2**: Visits each restaurant page individually for detailed information extraction

### 🌍 Multi-Language Support
Automatically detects and sets the appropriate language based on location:
- 🇺🇸 English (US, UK, AU)
- 🇯🇵 Japanese
- 🇫🇷 French
- 🇩🇪 German
- 🇪🇸 Spanish
- 🇮🇹 Italian
- 🇨🇳 Chinese
- 🇰🇷 Korean
- 🇷🇺 Russian
- 🇮🇳 Hindi
- 🇦🇪 Arabic
- ...and more!

### 📊 Comprehensive Data Extraction (20+ Fields)

#### Basic Information
- ✅ Restaurant Name
- ⭐ Rating (out of 5)
- 💬 Total Review Count
- 💰 Price Range ($, $$, $$$, $$$$)
- 🍽️ Cuisine Type

#### Detailed Information
- 📝 Full Description
- 🚗 Service Options (Dine-in, Takeout, Delivery, No-contact delivery)
- 📍 Complete Address
- 🕐 Current Status (Open/Closed)
- ⏰ Hours Summary
- 📞 Phone Number
- 🌐 Official Website
- 🔗 Menu Link
- 📅 Reservation Link
- 📍 Google Plus Code
- ♿ Accessibility Features
- 📈 Popular Times Availability
- 💭 Recent Review Snippet
- 🔗 Google Maps URL

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (automatically managed by Selenium)

### Step 1: Install Required Packages

```bash
pip install selenium pandas openpyxl
```

### Step 2: Download the Script
Save the `3_listings_with_details.py` file to your project directory.

## 💻 Usage

### Basic Usage

```python
from selenium import webdriver
# Import the scraper class (ensure the script is in your directory)

scraper = GoogleMapsDetailedScraper()

try:
    # Scrape restaurants from any location
    query = "restaurants in new york"
    complete_data = scraper.scrape_complete_data(query)
    
    # Export to Excel
    scraper.export_to_excel(complete_data, 'newyork_restaurants.xlsx')
    
finally:
    scraper.close()
```

### Advanced Examples

#### Example 1: Pizza Places in Chicago
```python
scraper = GoogleMapsDetailedScraper()
try:
    data = scraper.scrape_complete_data("pizza in chicago")
    scraper.export_to_excel(data, 'chicago_pizza.xlsx')
finally:
    scraper.close()
```

#### Example 2: Sushi Restaurants in Tokyo
```python
scraper = GoogleMapsDetailedScraper()
try:
    data = scraper.scrape_complete_data("sushi restaurants in tokyo")
    scraper.export_to_excel(data, 'tokyo_sushi.xlsx')
finally:
    scraper.close()
```

#### Example 3: Vegan Cafes in London
```python
scraper = GoogleMapsDetailedScraper()
try:
    data = scraper.scrape_complete_data("vegan cafes in london")
    scraper.export_to_excel(data, 'london_vegan_cafes.xlsx')
finally:
    scraper.close()
```

## 📁 Output Format

The scraper exports data to a clean, organized Excel file with the following columns:

| Column | Description |
|--------|-------------|
| name | Restaurant name |
| rating | Star rating (1-5) |
| total_reviews | Total number of reviews |
| price_range | Price level ($-$$$$) |
| cuisine_type | Type of cuisine |
| description | Full restaurant description |
| service_options | Available services (dine-in, takeout, etc.) |
| address | Complete address |
| current_status | Open/Closed status |
| hours_summary | Operating hours |
| phone | Contact number |
| website | Official website URL |
| menu_link | Link to menu |
| reservation_link | Online reservation link |
| plus_code | Google Plus Code |
| accessibility | Accessibility features |
| has_popular_times | Popular times data available |
| recent_review | Snippet from recent review |
| url | Google Maps listing URL |
| detail_url | Direct link to detailed page |

## 🎯 Use Cases

### 1. **Market Research**
- Analyze restaurant density in specific areas
- Study pricing strategies by cuisine type
- Identify service option trends

### 2. **Business Intelligence**
- Competitive analysis for restaurant owners
- Location scouting for new establishments
- Service gap identification

### 3. **Data Analysis Projects**
- Rating correlation studies
- Price vs. rating analysis
- Popular cuisine trends by city

### 4. **Lead Generation**
- Build contact databases
- Create targeted marketing lists
- Identify businesses without websites

### 5. **Academic Research**
- Urban planning studies
- Consumer behavior analysis
- Geographic business distribution

## ⚙️ Technical Features

### Smart Scrolling Algorithm
- Automatically scrolls through all results
- Detects end of list intelligently
- Prevents infinite loops with max scroll limit

### Robust Error Handling
- Gracefully handles missing data
- Continues scraping even if individual elements fail
- Provides detailed error logging

### Rate Limiting
- Built-in delays between requests
- Respects website usage policies
- Prevents IP blocking

### Anti-Detection Measures
- Disables automation flags
- Mimics human browsing behavior
- Randomized wait times

## 📊 Performance

- **Average speed**: 3-5 seconds per restaurant (detailed page)
- **Recommended batch size**: 50-100 restaurants per session
- **Success rate**: 95%+ for active listings

## ⚠️ Important Notes

### Legal & Ethical Use
- ✅ For personal research and analysis
- ✅ For academic studies
- ✅ For business intelligence
- ❌ Do not scrape for commercial resale of raw data
- ❌ Respect robots.txt and terms of service
- ❌ Do not overload servers with excessive requests

### Best Practices
1. **Use reasonable delays** between requests (2-3 seconds minimum)
2. **Limit batch sizes** to avoid detection
3. **Run during off-peak hours** when possible
4. **Store data responsibly** and respect privacy
5. **Verify data accuracy** before business use

### Limitations
- Requires active internet connection
- Chrome browser must be installed
- Some data may be unavailable for certain listings
- Popular times data requires additional parsing
- May need periodic updates due to Google Maps UI changes

## 🛠️ Troubleshooting

### Common Issues

**Issue**: ChromeDriver version mismatch
```bash
# Solution: Update selenium to auto-manage drivers
pip install --upgrade selenium
```

**Issue**: Elements not found
- **Cause**: Google Maps UI update
- **Solution**: Check CSS selectors in the code and update if needed

**Issue**: Slow scraping
- **Solution**: Reduce `time.sleep()` values carefully (maintain 2+ seconds)

**Issue**: No results found
- **Solution**: Verify query syntax and check internet connection

## 📈 Future Enhancements

- [ ] Review sentiment analysis
- [ ] Image download capability
- [ ] Menu item extraction
- [ ] Historical rating tracking
- [ ] CSV export option
- [ ] Multi-threaded scraping
- [ ] Proxy rotation support
- [ ] GUI interface

## 🤝 Support

For issues, questions, or feature requests, please contact the developer or open an issue in the repository.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚡ Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Chrome browser installed
- [ ] Required packages installed (`pip install selenium pandas openpyxl`)
- [ ] Script downloaded to project directory
- [ ] Test query prepared
- [ ] Output filename decided
- [ ] Ready to scrape!

---

## 🎓 Example Output Preview

```
=========================================================
STEP 1: Scraping restaurant list from Google Maps
=========================================================
Using language code: en-US for query: restaurants in new york
Opening URL: https://www.google.com/maps/search/restaurants+in+new+york
Scrolling to load all results...
Found 87 restaurants

=========================================================
STEP 2: Scraping detailed information from each restaurant
=========================================================
[1/87] Processing: The Modern
Scraping details from: https://www.google.com/maps/place/...
[2/87] Processing: Le Bernardin
Scraping details from: https://www.google.com/maps/place/...

=========================================================
Data exported to newyork_restaurants_complete.xlsx
Total restaurants scraped: 87
=========================================================
```

---

**Made with ❤️ for data enthusiasts and business researchers**

*Scrape smarter, not harder!*