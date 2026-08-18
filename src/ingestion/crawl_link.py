import pandas as pd
from bs4 import BeautifulSoup
import requests
LISTING_URL = "https://xe.chotot.com/mua-ban-oto"
N_pages = 1200

def crawl_link_list():
    all_car_link = []
    for i in range(1001, N_pages + 1):
        url = f"{LISTING_URL}?page={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        car_links = soup.find_all("a", class_="c15fd2pn")
        print(f"Crawling page: {i}. Found {len(car_links)} car links.")
        for link in car_links:
            all_car_link.append(LISTING_URL +link.get("href"))
    return all_car_link

def save_link_list_to_csv(car_links, filename):
    df = pd.DataFrame({
        "id": range(1, len(car_links) + 1),
        "Link": car_links
    })
    df.to_csv(filename, mode = 'a' , index=False)


if __name__ == "__main__":
    car_links = crawl_link_list()
    save_link_list_to_csv(car_links, "/home/khanhdo/Documents/project/chotot-pipeline/data/data_ingestion/car_links.csv")
    print(f"Total car links found: {len(car_links)}")