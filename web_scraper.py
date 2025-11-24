import os
import sys
import subprocess
import pandas as pd
from config.sites import SUPPORTED_SITES

# --- Package Installation and Check ---

REQUIRED_PACKAGES = ['requests', 'pandas', 'openpyxl', 'urllib3']

def display_header():
    """Prints a styled header for the CLI application using a raw string."""
    # Using a raw string (r"...") prevents Python from interpreting backslashes 
    # in the ASCII art as escape sequences, fixing the SyntaxWarning and display issues.
    header = r"""
    _______________________________________________________________
    
      ___          __    _______   ________ 
     |\  \        |\  \|\  ___ \ |\  __  \ 
     \ \  \       \ \  \ \  __\ \ \  \|\ /_ 
      \ \  \  __\ \  \ \  \_|/_\ \  __  \ 
       \ \  \|\__\_\  \ \  \_|\ \ \  \|\  \ 
        \ \____________\ \_______\ \_______\ 
       __________________\|________\|________  ________  _______   ________ 
      |\  ____\|\  ____\|\  __  \|\  __  \|\  __  \|\  ___ \ |\  __  \ 
      \ \  \___|\ \  \___|\ \  \|\  \ \  \|\  \ \  \|\  \ \  __\ \  \|\  \ 
       \ \_____  \ \  \    \ \  _  _\ \  __  \ \  ____\ \  \_|/_\ \  _  _\ 
        \|____|\  \ \  \____\ \  \\  \\ \  \ \  \ \  \___|\ \  \_|\ \ \  \\  \| 
          ____\_\  \ \_______\ \__\\ _\\ \__\ \__\ \__\    \ \_______\ \__\\ _\ 
         |\_________\|_______|\|__|\|__|\|__|\|__|\|__|    \|_______|\|__|\|__|
         \|_________| 
                       ><>< Developed by Chamicara De Silva ><><
    _______________________________________________________________
    """
    print(header)

def check_dependencies():
    """Checks if all packages listed in requirements.txt are installed."""
    print("--- 1. Checking Dependencies ---")
    all_installed = True

    sys.stdout.flush()

    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            print(f"  [ OK ] {package}")
        except ImportError:
            print(f"  [FAIL] {package}. Please run 'pip install -r requirements.txt'")
            all_installed = False
            
    if not all_installed:
        print("\nDependencies missing. Please install required packages before proceeding.")
        sys.exit(1)
    
    print("\n✅ Dependencies check passed.")

def get_user_choice():
    """Prompts the user to select a country and a website."""
    
    countries = list(SUPPORTED_SITES.keys())
    if not countries:
        print("\nError: No supported countries defined in config/sites.py. Exiting.")
        sys.exit(1)
        
    print("\n--- 2. Select Country ---")
    
    for i, country_name in enumerate(countries, 1):
        print(f"  {i}. {country_name}")
        
    try:
        if len(countries) > 1:
            country_choice = int(input("Enter country number: "))
            selected_country = countries[country_choice - 1]
        else:
            print(f"  (Defaulting to: {countries[0]})")
            selected_country = countries[0]
            
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        sys.exit(1)
        
    sites_in_country = SUPPORTED_SITES[selected_country]
    
    print(f"\n--- 3. Select Website (Country: {selected_country}) ---")
    
    site_names = list(sites_in_country.keys())
    for i, name in enumerate(site_names, 1):
        print(f"  {i}. {name}")
        
    try:
        site_choice = int(input("Enter website number: "))
        if 1 <= site_choice <= len(site_names):
            site_name = site_names[site_choice - 1]
            return sites_in_country[site_name]
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)
    except ValueError:
        print("Invalid input. Please enter a number. Exiting.")
        sys.exit(1)


def save_data(data, config):
    """Saves the scraped data to an Excel file using pandas."""
    filename = config['output_filename']
    if not data:
        print("No data was scraped to save.")
        return

    print(f"\n--- 4. Saving Data to {filename} ---")
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl') 
        print(f"✅ SUCCESS: Data saved to {filename}")
        print(f"Total records saved: {len(data)}")
    except Exception as e:
        print(f"❌ ERROR: Failed to save to Excel. Details: {e}")

if __name__ == "__main__":
    
    display_header()
    
    check_dependencies()
    
    chosen_site = get_user_choice()
    
    scraper_function = chosen_site['scraper']
    scraper_config = chosen_site['config']
    
    print("\n--- 4. Running Scraper ---")
    scraped_data = scraper_function(scraper_config)
    
    save_data(scraped_data, scraper_config)
    
    print("\n--------------------------------------------------------------")
    print("✨ Bye now ! Have a great day.")
    print("--------------------------------------------------------------")