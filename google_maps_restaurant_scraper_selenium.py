from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import re

class GoogleMapsDetailedScraper:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self, language_code='en'):
        """Setup Chrome driver with language preferences"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set language preference
        prefs = {
            "intl.accept_languages": language_code,
            "profile.default_content_setting_values.geolocation": 1
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        
    def get_language_code(self, query):
        """Detect language code based on query location"""
        location_lang_map = {
            'new york': 'en-US',
            'tokyo': 'ja-JP',
            'paris': 'fr-FR',
            'berlin': 'de-DE',
            'madrid': 'es-ES',
            'rome': 'it-IT',
            'beijing': 'zh-CN',
            'seoul': 'ko-KR',
            'moscow': 'ru-RU',
            'london': 'en-GB',
            'sydney': 'en-AU',
            'mumbai': 'hi-IN',
            'dubai': 'ar-AE',
        }
        
        query_lower = query.lower()
        for location, lang_code in location_lang_map.items():
            if location in query_lower:
                return lang_code
        
        return 'en-US'
    
    def scroll_to_load_all(self, scrollable_div, pause_time=2):
        """Scroll through the results panel to load all data"""
        print("Scrolling to load all results...")
        
        last_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", scrollable_div
        )
        
        scroll_count = 0
        max_scrolls = 50
        
        while scroll_count < max_scrolls:
            self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight);", 
                scrollable_div
            )
            
            time.sleep(pause_time)
            
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", scrollable_div
            )
            
            if new_height == last_height:
                scroll_count += 1
                if scroll_count >= 3:
                    print(f"Reached end of results")
                    break
            else:
                scroll_count = 0
                
            last_height = new_height
            
        print("Finished scrolling")
    
    def scrape_restaurant_list(self, query):
        """Scrape basic restaurant information from search results"""
        lang_code = self.get_language_code(query)
        print(f"Using language code: {lang_code} for query: {query}")
        
        self.setup_driver(lang_code)
        
        try:
            base_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            url = f"{base_url}?hl={lang_code.split('-')[0]}"
            
            print(f"Opening URL: {url}")
            self.driver.get(url)
            
            wait = WebDriverWait(self.driver, 15)
            scrollable_div = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
            )
            
            self.scroll_to_load_all(scrollable_div)
            
            time.sleep(2)
            restaurants = self.driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
            
            print(f"Found {len(restaurants)} restaurants")
            
            data = []
            
            for idx, restaurant in enumerate(restaurants, 1):
                try:
                    print(f"Scraping basic info for restaurant {idx}/{len(restaurants)}")
                    
                    restaurant_data = {}
                    
                    # Name
                    try:
                        name = restaurant.find_element(By.CSS_SELECTOR, ".qBF1Pd").text
                        restaurant_data['name'] = name
                    except:
                        restaurant_data['name'] = 'N/A'
                    
                    # URL - Most important for detailed scraping
                    try:
                        link = restaurant.find_element(By.CSS_SELECTOR, "a.hfpxzc")
                        restaurant_data['url'] = link.get_attribute('href')
                    except:
                        restaurant_data['url'] = 'N/A'
                    
                    # Rating
                    try:
                        rating = restaurant.find_element(By.CSS_SELECTOR, ".MW4etd").text
                        restaurant_data['rating'] = rating
                    except:
                        restaurant_data['rating'] = 'N/A'
                    
                    # Number of reviews
                    try:
                        reviews = restaurant.find_element(By.CSS_SELECTOR, ".UY7F9").text
                        restaurant_data['reviews_count'] = reviews.strip('()')
                    except:
                        restaurant_data['reviews_count'] = 'N/A'
                    
                    data.append(restaurant_data)
                    
                except Exception as e:
                    print(f"Error scraping restaurant {idx}: {str(e)}")
                    continue
            
            return data
            
        except Exception as e:
            print(f"Error during list scraping: {str(e)}")
            return []
    
    def scrape_detailed_info(self, url):
        """Scrape detailed information from individual restaurant page"""
        print(f"Scraping details from: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            detailed_data = {}
            
            # Restaurant Name
            try:
                name = self.driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
                detailed_data['name'] = name
            except:
                detailed_data['name'] = 'N/A'
            
            # Rating
            try:
                rating = self.driver.find_element(By.CSS_SELECTOR, ".F7nice span[aria-hidden='true']").text
                detailed_data['rating'] = rating
            except:
                detailed_data['rating'] = 'N/A'
            
            # Total Reviews
            try:
                reviews = self.driver.find_element(By.CSS_SELECTOR, ".F7nice span[role='img']").get_attribute('aria-label')
                # Extract number from aria-label
                reviews_match = re.search(r'([\d,]+)', reviews)
                if reviews_match:
                    detailed_data['total_reviews'] = reviews_match.group(1)
                else:
                    detailed_data['total_reviews'] = 'N/A'
            except:
                detailed_data['total_reviews'] = 'N/A'
            
            # Price Range
            try:
                price = self.driver.find_element(By.CSS_SELECTOR, ".mgr77e span").text
                detailed_data['price_range'] = price
            except:
                detailed_data['price_range'] = 'N/A'
            
            # Cuisine Type
            try:
                cuisine = self.driver.find_element(By.CSS_SELECTOR, "button.DkEaL").text
                detailed_data['cuisine_type'] = cuisine
            except:
                detailed_data['cuisine_type'] = 'N/A'
            
            # Description
            try:
                description = self.driver.find_element(By.CSS_SELECTOR, ".PYvSYb").text
                detailed_data['description'] = description
            except:
                detailed_data['description'] = 'N/A'
            
            # Service Options (Dine-in, Takeout, Delivery)
            try:
                service_options = []
                service_elements = self.driver.find_elements(By.CSS_SELECTOR, ".LTs0Rc div[aria-hidden='true']")
                for elem in service_elements:
                    service_options.append(elem.text)
                detailed_data['service_options'] = ', '.join(service_options) if service_options else 'N/A'
            except:
                detailed_data['service_options'] = 'N/A'
            
            # Address
            try:
                address = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address'] .Io6YTe").text
                detailed_data['address'] = address
            except:
                detailed_data['address'] = 'N/A'
            
            # Hours
            try:
                hours_button = self.driver.find_element(By.CSS_SELECTOR, ".OMl5r.hH0dDd")
                # Check if it's open or closed
                status = self.driver.find_element(By.CSS_SELECTOR, ".ZDu9vd span").text
                detailed_data['current_status'] = status
                
                # Try to get hours summary
                hours_summary = self.driver.find_element(By.CSS_SELECTOR, ".ZDu9vd").text
                detailed_data['hours_summary'] = hours_summary
            except:
                detailed_data['current_status'] = 'N/A'
                detailed_data['hours_summary'] = 'N/A'
            
            # Phone Number
            try:
                phone = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id^='phone'] .Io6YTe").text
                detailed_data['phone'] = phone
            except:
                detailed_data['phone'] = 'N/A'
            
            # Website
            try:
                website = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']").get_attribute('href')
                detailed_data['website'] = website
            except:
                detailed_data['website'] = 'N/A'
            
            # Plus Code
            try:
                plus_code = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='oloc'] .Io6YTe").text
                detailed_data['plus_code'] = plus_code
            except:
                detailed_data['plus_code'] = 'N/A'
            
            # Menu Link
            try:
                menu_link = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='menu']").get_attribute('href')
                detailed_data['menu_link'] = menu_link
            except:
                detailed_data['menu_link'] = 'N/A'
            
            # Reservation Link
            try:
                reservation_link = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='action:1']").get_attribute('href')
                detailed_data['reservation_link'] = reservation_link
            except:
                detailed_data['reservation_link'] = 'N/A'
            
            # Popular Times (if available)
            try:
                popular_times_available = len(self.driver.find_elements(By.CSS_SELECTOR, ".UmE4Qe")) > 0
                detailed_data['has_popular_times'] = 'Yes' if popular_times_available else 'No'
            except:
                detailed_data['has_popular_times'] = 'No'
            
            # Accessibility
            try:
                accessibility_features = []
                accessibility_icons = self.driver.find_elements(By.CSS_SELECTOR, "span.google-symbols[data-tooltip*='accessible']")
                for icon in accessibility_icons:
                    accessibility_features.append(icon.get_attribute('data-tooltip'))
                detailed_data['accessibility'] = ', '.join(accessibility_features) if accessibility_features else 'N/A'
            except:
                detailed_data['accessibility'] = 'N/A'
            
            # Recent Review Snippet
            try:
                recent_review = self.driver.find_element(By.CSS_SELECTOR, ".MyEned .wiI7pd").text
                detailed_data['recent_review'] = recent_review[:200]  # First 200 chars
            except:
                detailed_data['recent_review'] = 'N/A'
            
            detailed_data['detail_url'] = url
            
            return detailed_data
            
        except Exception as e:
            print(f"Error scraping details from {url}: {str(e)}")
            return {'detail_url': url, 'error': str(e)}
    
    def scrape_complete_data(self, query):
        """Complete scraping: list + details for each restaurant"""
        print("=" * 60)
        print("STEP 1: Scraping restaurant list from Google Maps")
        print("=" * 60)
        
        # Step 1: Get basic restaurant list
        restaurant_list = self.scrape_restaurant_list(query)
        
        if not restaurant_list:
            print("No restaurants found!")
            return []
        
        print(f"\nFound {len(restaurant_list)} restaurants")
        print("=" * 60)
        print("STEP 2: Scraping detailed information from each restaurant")
        print("=" * 60)
        
        # Step 2: Get detailed info for each restaurant
        complete_data = []
        
        for idx, restaurant in enumerate(restaurant_list, 1):
            url = restaurant.get('url')
            
            if url and url != 'N/A':
                print(f"\n[{idx}/{len(restaurant_list)}] Processing: {restaurant.get('name', 'Unknown')}")
                
                # Get detailed information
                detailed_info = self.scrape_detailed_info(url)
                
                # Merge basic and detailed info
                combined_data = {**restaurant, **detailed_info}
                complete_data.append(combined_data)
                
                # Small delay between requests
                time.sleep(2)
            else:
                print(f"\n[{idx}/{len(restaurant_list)}] Skipping {restaurant.get('name', 'Unknown')} - No URL")
                complete_data.append(restaurant)
        
        return complete_data
    
    def export_to_excel(self, data, filename='google_maps_complete_data.xlsx'):
        """Export complete scraped data to Excel"""
        if not data:
            print("No data to export")
            return
        
        df = pd.DataFrame(data)
        
        # Reorder columns for better readability
        preferred_order = [
            'name', 'rating', 'total_reviews', 'reviews_count', 'price_range', 
            'cuisine_type', 'description', 'service_options', 'address', 
            'current_status', 'hours_summary', 'phone', 'website', 'menu_link', 
            'reservation_link', 'plus_code', 'accessibility', 'has_popular_times',
            'recent_review', 'url', 'detail_url'
        ]
        
        # Only include columns that exist
        column_order = [col for col in preferred_order if col in df.columns]
        remaining_cols = [col for col in df.columns if col not in column_order]
        column_order.extend(remaining_cols)
        
        df = df[column_order]
        
        # Export to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n{'=' * 60}")
        print(f"Data exported to {filename}")
        print(f"Total restaurants scraped: {len(df)}")
        print(f"{'=' * 60}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    scraper = GoogleMapsDetailedScraper()
    
    try:
        # Scrape complete data for New York restaurants
        query = "restaurants in new york"
        complete_data = scraper.scrape_complete_data(query)
        
        # Export to Excel
        scraper.export_to_excel(complete_data, 'newyork_restaurants_complete.xlsx')
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
    
    finally:
        # Always close the browser
        scraper.close()