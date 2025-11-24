from scrapers import buyabans

SUPPORTED_SITES = {
    "Sri Lanka": {
        "BuyAbans.com (All Products)": {
            "scraper": buyabans.scrape_buyabans,
            "config": {
                "base_url": "https://buyabans.com/product-list",
                "category_ids": [
                    '67', '567', '9', '568', '569', '570', '572', 
                    '573', '27', '19', '26', '17', '33'
                ],
                "output_filename": "BuyAbans_All_Products.xlsx",
                "country": "Sri Lanka",
                "year": 2025,
                "min_price": 1000,
                "max_price": 99999999
            }
        },
    }
}
