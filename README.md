🌐 Price Scraper CLI (Sri Lanka Focus)

A modular, command-line utility designed for fast, resilient scraping of product data from e-commerce websites in supported regions, currently focused on Sri Lanka.

✨ Features & Resilience

Modular Architecture: Easily extensible by adding new site-specific scraper modules.

Initial Coverage: Supports scraping all major categories from BuyAbans.com.

Resilience: Implements automatic request retries (handling 504 Gateway Timeouts) and polite scraping delays.

Data Integrity: Robust brand extraction logic ensures accurate product attribution, even if the source JSON is messy.

User Interface: Interactive CLI guides users through dependency checks and site selection.

Output: Exports clean, structured data directly to .xlsx (Excel) files.

🚀 Getting Started

1. Prerequisites

You need Python 3.8+ installed on your system.

2. Installation

First, clone the repository to your local machine:

git clone [https://github.com/Optane002/web_scraper.git](https://github.com/Optane002/web_scraper.git)
cd web_scraper


Next, install all required Python packages (requests, pandas, openpyxl, urllib3):

pip install -r requirements.txt


3. Running the Scraper

Execute the main script from the root directory of the project:

python web_scraper.py


The application will run its checks and then present an interactive menu for you to select the country and the target website.

⚙️ Project Structure & Extensibility

The application is split into clear components, allowing simple contribution:

web_scraper/
├── config/
│   └── sites.py        # Maps countries/sites to their scraper functions and configuration settings.
├── scrapers/
│   ├── __init__.py     # Package initializer.
│   └── mysite.py     # **Contains site-specific scraping logic and helpers.**
├── web_scraper.py      # Main CLI entry point, handling headers, checks, and user flow.
├── requirements.txt    # Lists all mandatory dependencies.
└── README.md


Contributing: Adding a New Website

The core principle of this project is easy extensibility. To add support for a new website (e.g., mysite.lk):

Create a Scraper Module:

Create a new file in the scrapers/ directory (e.g., mysite.py).

Implement the main scraper function (it must accept a config dictionary and return a list of product dictionaries).

Integrate:

Import your new scraper function into scrapers/__init__.py.

Add a new entry to the SUPPORTED_SITES dictionary in config/sites.py, providing the necessary configuration (Base URL, specific IDs, file names, etc.).

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
