import pandas as pd
from bs4 import BeautifulSoup
import requests
from pathlib import Path

DATA_DIR = Path("/home/khanhdo/Documents/project/chotot-pipeline/data/data_ingestion")
CAR_LINKS_FILE = DATA_DIR / "car_links.csv"
CAR_DETAILS_FILE = DATA_DIR / "car_details.csv"
CHECKPOINT_FILE = DATA_DIR / "checkpoint.txt"

def load_checkpoint():
    if not CHECKPOINT_FILE.exists():
        return 0

    content = CHECKPOINT_FILE.read_text().strip()
    return int(content) if content else 0

def save_checkpoint(current_id):
    CHECKPOINT_FILE.write_text(str(current_id))

def save_car_detail(car_details):
    df = pd.DataFrame([car_details])
    df.to_csv(
        CAR_DETAILS_FILE,
        mode="a",
        index=False,
        header=not CAR_DETAILS_FILE.exists(),
    )

def get_info_by_itemprop(soup, itemprop):
    element = soup.find("span", itemprop=itemprop)
    return element.text.strip() if element else None

def crawl_car_details(car_link):
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
    return car_info

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    car_links = pd.read_csv(CAR_LINKS_FILE)["Link"].dropna().tolist()
    checkpoint = load_checkpoint()

    print(f"Loaded {len(car_links)} links.")
    print(f"Continue from id: {checkpoint + 1}")

    for idx, link in enumerate(car_links, start=1):
        if idx <= checkpoint:
            continue

        car_details = crawl_car_details(link)
        save_car_detail(car_details)
        save_checkpoint(idx)
        if idx % 1000 == 0:
            print(f"Crawled to id {idx}...")

    print(f"Done. Last checkpoint: {load_checkpoint()}")
