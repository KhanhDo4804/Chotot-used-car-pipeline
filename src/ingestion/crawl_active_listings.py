from datetime import datetime, timezone
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, urlunsplit

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LISTING_URL = "https://xe.chotot.com/mua-ban-oto"
N_PAGES = 1000
OUTPUT_PATH = "data/data_cdc/active_listings.parquet"
EMPTY_PAGE_LIMIT = 5
MIN_LISTINGS = 100


def split_id(link):
    a = link.split("/")
    x = a[-1]
    return x[:9]


def build_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "Chrome/124.0 Safari/537.36"
            )
        }
    )
    return session


def extract_listing_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for anchor in soup.select("a[href]"):
        href = anchor.get("href")
        if not href:
            continue

        parsed_link = urlsplit(urljoin(LISTING_URL, href))
        link = urlunsplit(
            (parsed_link.scheme, parsed_link.netloc, parsed_link.path, "", "")
        )
        listing_id = split_id(link)
        if listing_id.isdigit() and len(listing_id) == 9:
            links.append(link)

    return list(dict.fromkeys(links))


def crawl_active_listings(n_pages=N_PAGES, output_path=OUTPUT_PATH):
    session = build_session()
    crawled_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    listings = {}
    consecutive_empty_pages = 0

    for page in range(1, n_pages + 1):
        response = session.get(
            LISTING_URL,
            params={"page": page},
            timeout=30,
        )
        response.raise_for_status()
        page_links = extract_listing_links(response.text)
        print(f"Crawling listing page {page}/{n_pages}: {len(page_links)} links")

        if page_links:
            consecutive_empty_pages = 0
            for link in page_links:
                listings[split_id(link)] = link
        else:
            consecutive_empty_pages += 1
            if consecutive_empty_pages >= EMPTY_PAGE_LIMIT:
                print(f"Stopping after {EMPTY_PAGE_LIMIT} consecutive empty pages.")
                break

        sleep(0.1)

    if len(listings) < MIN_LISTINGS:
        raise RuntimeError(
            f"Only {len(listings)} active listing IDs were found; expected at least "
            f"{MIN_LISTINGS}. Refusing to publish an incomplete snapshot."
        )

    dataframe = pd.DataFrame(
        [
            {"listing_id": listing_id, "link": link, "crawled_at": crawled_at}
            for listing_id, link in listings.items()
        ]
    )
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(output_file, index=False)
    print(f"Saved {len(dataframe)} active listings to {output_file}")
    return output_file


if __name__ == "__main__":
    crawl_active_listings()
