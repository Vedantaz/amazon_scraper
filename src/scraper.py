import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv


# function to scrap Amazon data
load_dotenv()


def scrape_amazon(search_query):
    # create a session
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        return ValueError("API token is missing, Please set it in env variables")
    # smart proxy scraper api url
    api_url = "http://api.scrape.do?token={api_token}"
    search_term = "laptops"
    target_url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"

    scrape_url = f"{api_url}&url={target_url}"

    response = requests.get(scrape_url)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        return None
    # payload and urls

    soup = BeautifulSoup(response.text, "html-parser")

    # extract details now

    products = []
    for item in soup.select('.s-main-slot .s-result-item'):
        title = item.select_one('h2 .a-link-normal')
        price = item.select_one('.a-price-whole')
        if title and price:
            products.append({'Title' : title.text.strip(), 'Price':price.text.strip()})
        
        return products
    payload = {"url" : target_url}
    headers = {
        "accept" : "application/json",
        "content-type" : "application/json",
        "authorization":""
    }

    # main function to execute the scraper
    if __name__ == "__main__":
        search_query = "laptops"
        results = scrape_amazon(search_query)

        if results:
                df = pd.DataFrame(results)
                df.to_csv("amazon_products.csv", index=False)
                return ("Scraped data saved to amazon_products.csv")
        else:
            print('No data scraped')

