import pandas as pd
import re
from pathlib import Path

def text_cleaning(text):
    text = re.sub(r"[^a-zA-Z0-9À-ỹ\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def number_cleaning(num):
    if pd.isna(num):
        return None
    if isinstance(num, (int, float)):
        return int(num)
    num = re.sub(r"[^\d]", "", str(num))
    return int(num) if num else None

def clean_address(address):
    address_parts = address.split(",")
    return text_cleaning(address_parts[-1].strip())

def split_id(link):
    a = link.split('/')
    x = a[-1]
    return x[:9]

def clean_car_details(df):
    df['listing_id'] = df['Link'].apply(split_id)
    df = df.drop_duplicates(subset=["Link"], keep="first")
    df = df.dropna(subset=["Link", "Tên", "Giá", "Địa chỉ", "Số KM đã đi"])
    df["Tên"] = df["Tên"].apply(text_cleaning)
    df["Giá"] = df["Giá"].apply(number_cleaning)
    df["Số KM đã đi"] = df["Số KM đã đi"].apply(number_cleaning)
    df["Địa chỉ"] = df["Địa chỉ"].apply(clean_address)
    return df


def clean_car_details_file(
    input_path="data/data_cdc/car_details.csv",
    output_path="data/data_cleaning/cleaned_car_details.parquet",
):
    car_details = pd.read_csv(input_path)
    cleaned_car_details = clean_car_details(car_details)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned_car_details.to_parquet(output_file, index=False)
    return output_file


if __name__ == "__main__":
    clean_car_details_file()



    
