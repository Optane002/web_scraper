import requests
from bs4 import BeautifulSoup
import re
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# --- Brand Helpers ---

KNOWN_BRANDS = [
    'HP', 'Lenovo', 'Asus', 'Acer', 'Dell', 'MSI', 'Apple', 
    'Samsung', 'LG', 'JVC', 'Haier', 'Toshiba', 'Electrolux', 
    'Whirlpool', 'Oppo', 'Xiaomi', 'JBL', 'Titan', 'Miniso',
    'Singer', 'Sony', 'Panasonic', 'Hitachi', 'Beko', 'Huawei',
    'TCL', 'Sharp', 'Kenwood', 'Sisil', 'Unic'
]

def extract_brand_from_name(product_name):
    """Tries to find a known brand name in the product title."""
    name_lower = product_name.lower()
    for brand in KNOWN_BRANDS:
        if brand.lower() in name_lower:
            return brand
    return 'Other'

def setup_session():
    """Configures a session with retry logic."""
    retry_strategy = Retry(
        total=3, 
        backoff_factor=1, 
        status_forcelist=[500, 502, 503, 504, 524], 
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    return http

# --- Main Scraper Function ---

def scrape_singer_sl(config):
    """
    Scrapes product data from SingerSL.com products page.
    """
    all_products_data = []
    session = setup_session()
    base_url = config['base_url']
    page = 1
    
    # Headers to mimic a real browser
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"\n[Singer SL] Starting scrape for {config['country']}...")
    
    while True:
        # Construct URL: Singer uses ?page=1, ?page=2 parameter
        current_url = f"{base_url}?page={page}"
        print(f"-> Fetching page {page}...")
        
        try:
            response = session.get(current_url, headers=HEADERS)
            response.raise_for_status() 
            soup = BeautifulSoup(response.content, 'html.parser')

            # 1. Product Container
            # Based on provided HTML: <div class="... product ...">
            # We look for the wrapper div that contains the productfilter class
            product_cards = soup.find_all('div', class_='product')

            if not product_cards:
                print("  No products found on this page. Stopping scrape.")
                break

            items_found_on_page = 0

            for card in product_cards:
                # 2. Extract Name
                # Title is in <h5 class="card-title product__name ...">
                name_elem = card.find('h5', class_='product__name')
                name = name_elem.text.strip() if name_elem else "N/A"
                
                # 3. Extract Price
                # Price is in <span class="price"> Rs 29,969 ... </span>
                # Sometimes it has nested <span class="original-price"> which we want to ignore if getting selling price,
                # but usually the text inside .price directly is the selling price or contains it.
                price_elem = card.find('span', class_='price')
                
                price = None 
                if price_elem:
                    # Get text, but be careful of nested children if they exist. 
                    # For Singer, the selling price is often the first text node or just inside.
                    raw_price_text = price_elem.get_text(strip=True)
                    
                    try:
                        # Clean: Remove 'Rs', commas, spaces
                        cleaned_price = re.sub(r'[^\d]', '', raw_price_text.split('.')[0])
                        price = int(cleaned_price)
                    except ValueError:
                        pass 
                
                # 4. Determine Brand
                final_brand_name = extract_brand_from_name(name)

                # 5. Filter based on Price Range
                is_in_price_range = price is not None and config['min_price'] <= price <= config['max_price']

                if is_in_price_range:
                    all_products_data.append({
                        'Category': 'General', 
                        'Brand': final_brand_name,
                        'Model': name,
                        'Price (LKR)': price,
                        'Country': config['country'],
                        'Year (Target)': config['year']
                    })
                    items_found_on_page += 1

            # Check for Next Page
            # Singer uses <a class="next page-numbers" href="...">
            next_link = soup.find('a', class_='next', href=True)
            
            if next_link and items_found_on_page > 0:
                page += 1
                time.sleep(random.uniform(1, 3))
            else:
                print("  Reached the last page.")
                break

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("  Page not found (404). Stopping.")
                break
            print(f"  Error fetching page {page}: {e}.")
            break 
        except Exception as e:
            print(f"  An unexpected error occurred on page {page}: {e}.")
            break 
            
    print(f"\n[Singer SL] Scraping finished. Found {len(all_products_data)} products.")
    return all_products_data
