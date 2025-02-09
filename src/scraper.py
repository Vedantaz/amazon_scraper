import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def scrape_flipkart(search_query):
    # create a session
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        return ValueError("API token is missing, Please set it in env variables")
    # smart proxy scraper api url
    api_url = f"http://api.scrape.do?token={api_token}"
    search_term = "laptops"
    target_url = f"https://www.flipkart.com/search?q={search_term.replace(' ', '+')}"

    scrape_url = f"{api_url}&url={target_url}"

# make the get request
    response = requests.get(scrape_url)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        return None
    # payload and urls
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    # extract details now

    products = []
    for item in soup.select('div._58bkzq6e'):  # Parent container class
        title = item.text.strip() if item else None
        price = item.find_next('div', class_='_58bkzq6e').text.strip() if item else None

        if title and price:
            products.append({'Title': title, 'Price': price})

    return products
    # payload = {"url" : target_url}
    # headers = {
    #     "accept" : "application/json",
    #     "content-type" : "application/json",
    #     "authorization":""
    # }

    # main function to execute the scraper
if __name__ == "__main__":
        search_query = "laptops"
        results = scrape_flipkart(search_query)

        if results:
                df = pd.DataFrame(results)
                output_file = "flipkart_products.csv"
                df.to_csv(output_file , index=False)
                print(f"Scraped data saved to flipkart_products.csv")
                
        else:
            print('No data scraped')

