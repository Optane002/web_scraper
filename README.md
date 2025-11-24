Price Scraper CLI (for Sri Lanka)

A modular, command-line tool designed to scrape product data from various e-commerce websites in supported countries (currently focused on Sri Lanka). The architecture is designed for easy expansion by adding new scraper modules.

🚀 Getting Started

Follow these steps to set up and run the scraper on your local machine.

Prerequisites

You need Python 3.x installed on your system.

Installation

Clone the repository:

git clone [https://github.com/YourUsername/price-scraper-cli.git](https://github.com/YourUsername/price-scraper-cli.git)
cd price-scraper-cli


Install dependencies:
The required Python packages are listed in requirements.txt.

pip install -r requirements.txt


Running the Scraper

Execute the main script from your terminal:

python web_scraper.py


The application will guide you through the following steps:

Dependency Check: It verifies all necessary packages are installed.

Country Selection: (Currently defaults to Sri Lanka if only one option exists).

Website Selection: You will choose which supported website to scrape (e.g., BuyAbans.com).

Scraping: The scraper runs, fetches data across multiple pages/categories, and handles server timeouts with retry logic.

Output: The final data is saved to a clean Excel file (e.g., mywebsite_All_Products.xlsx).

⚙️ Project Structure & Extensibility

The tool uses a modular design to make adding new sites simple:

price-scraper-cli/
├── config/
│   └── sites.py        # Maps country/site names to scraper functions and configs
├── scrapers/
│   ├── __init__.py     # Makes 'scrapers' a Python package
│   └── buyabans.py     # **Site-specific logic for BuyAbans.com**
├── web_scraper.py      # Main CLI execution and dependency check
├── requirements.txt    # Project dependencies
└── README.md


Adding a New Website (e.g., mywebsite.lk)

Create a new file in the scrapers/ directory: scrapers/mywebsite.py.

Implement a single main function inside mywebsite.py that takes a config dictionary (just like scrape_exsitingfile does).

Import the new scraper function into scrapers/__init__.py.

Add a new entry to the SUPPORTED_SITES dictionary in config/sites.py, linking it to your new scraper function and providing the necessary configuration (base URL, specific categories, etc.).

No changes are needed in web_scraper.py! The main application automatically detects the new option.
