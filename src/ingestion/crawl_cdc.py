import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone
from pathlib import Path

LISTING_URL = "https://xe.chotot.com/mua-ban-oto"
N_pages = 3

def crawl_link_list(n_pages=N_pages):
    all_car_link = []
    for i in range(0, n_pages ):
        url = f"{LISTING_URL}?page={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        car_links = soup.find_all("a", class_="c15fd2pn")
        print(f"Crawling page: {i}. Found {len(car_links)} car links.")
        for link in car_links:
            all_car_link.append(LISTING_URL +link.get("href"))
    return all_car_link


def get_info_by_itemprop(soup, itemprop):
    element = soup.find("span", itemprop=itemprop)
    return element.text.strip() if element else None

def crawl_car_details(car_link, crawled_at):
    response = requests.get(car_link)
    soup_detail = BeautifulSoup(response.content, "html.parser")

    car_info = {}
    car_info["Link"] = car_link

    name = soup_detail.find("span", class_="BreadCrumb_breadcrumbLastItem__Bu4C8")
    car_info["Tên"] = name.text.strip() if name else None
            
    price = soup_detail.find("b", class_="p26z2wb")
    car_info["Giá"] = price.text.strip() if price else None

    addr = soup_detail.find("span", class_="bwq0cbs flex-1")
    car_info["Địa chỉ"] = addr.text.strip() if addr else None
            
    car_info['Số KM đã đi'] = get_info_by_itemprop(soup_detail, 'mileage_v2')
    car_info['Xuất xứ'] = get_info_by_itemprop(soup_detail, 'carorigin')
    car_info['Tình trạng'] = get_info_by_itemprop(soup_detail, 'condition_ad')
    car_info['Hãng'] = get_info_by_itemprop(soup_detail, 'carbrand')
    car_info['Dòng xe'] = get_info_by_itemprop(soup_detail, 'carmodel')
    car_info['Năm sản xuất'] = get_info_by_itemprop(soup_detail, 'mfdate')
    car_info['Hộp số'] = get_info_by_itemprop(soup_detail, 'gearbox')
    car_info['Nhiên liệu'] = get_info_by_itemprop(soup_detail, 'fuel')
    car_info['Kiểu dáng'] = get_info_by_itemprop(soup_detail, 'cartype')
    car_info['Số chỗ'] = get_info_by_itemprop(soup_detail, 'carseats')
    car_info["crawled_at"] = crawled_at
    return car_info

def crawl_cdc(output_path="data/data_cdc/car_details.csv", n_pages=N_pages):
    crawled_at = datetime.now(timezone.utc).replace(tzinfo=None)
    car_links = crawl_link_list(n_pages)
    print(f"Total car links found: {len(car_links)}")
    car_details_list = []
    for link in car_links:
        car_details = crawl_car_details(link, crawled_at)
        car_details_list.append(car_details)
    car_details_df = pd.DataFrame(car_details_list)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    car_details_df.to_csv(output_file, index=False)
    return output_file


if __name__ == "__main__":
    crawl_cdc()
