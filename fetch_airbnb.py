import gzip
import shutil
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse
import pandas as pd
import warnings
from pandas.errors import DtypeWarning
import sys
from datetime import datetime

warnings.filterwarnings("ignore", category=DtypeWarning)

# Ustawienie logowania do pliku
today_str = datetime.today().strftime('%Y%m%d%H%M%S')

log_path = fr"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\logs\1 fetch_airbnb\log_fetch_airbnb_{today_str}.txt"
#log_path = fr"\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\logs\1 fetch_airbnb\log_fetch_airbnb_{today_str}.txt"

log_file = open(log_path, mode="w", encoding="utf-8")

# Przekierowanie stdout i stderr do pliku
sys.stdout = log_file
sys.stderr = log_file

BASE_URL = "http://insideairbnb.com/get-the-data/"

DOWNLOAD_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data"
#DOWNLOAD_DIR = r"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\airbnb_data"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def normalize_filename(url):
    parts = urlparse(url).path.strip("/").split("/")

    try:
        if len(parts) >= 6:
            # Format standardowy: kraj / region / miasto / data / data / plik
            country = parts[0].replace(" ", "")
            region = parts[1].replace(" ", "")
            city = parts[2].replace(" ", "")
            date = parts[3].replace("-", "")  # YYYYMMDD
        elif len(parts) >= 4:
            # Format skrócony: kraj / data / data / plik
            country = parts[0].replace(" ", "")
            region = city = country  # używamy kraju jako "regionu" i "miasta"
            date = parts[1].replace("-", "")
        else:
            raise ValueError("Nieznany format URL")

        filename = parts[-1]
        if filename.endswith(".csv.gz"):
            filename = filename[:-3]  # usuń .gz

        return f"{date}_{country}_{region}_{city}_{filename}"

    except Exception as e:
        print(f"[!] Błąd przy tworzeniu nazwy dla {url}: {e}")
        return os.path.basename(url)


def extract_base_and_date(filename):
    match = re.match(r"(\d{8})_(.+)_(listings|calendar|reviews|neighbourhoods\.geojson)$", filename)
    if match:
        date = match.group(1)
        base = match.group(2)  # np. belgium_vlg_ghent
        typ = match.group(3)
        return f"{base}_{typ}", date
    else:
        parts = filename.split("_", 1)
        if len(parts) == 2:
            return parts[1], parts[0]
        return filename, "00000000"
    
def process_listings_csv(df):
    desired_columns = [
        "id",
        "last_scraped",
        "name",
        "host_id",
        "host_name",
        "host_since",
        "host_response_time",
        "host_response_rate",
        "host_acceptance_rate",
        "host_is_superhost",
        "host_listings_count",
        "host_total_listings_count",
        "host_identity_verified",
        "latitude",
        "longitude",
        "property_type",
        "room_type",
        "accommodates",
        "bathrooms",
        "bedrooms",
        "beds",
        "price",
        "minimum_nights",
        "maximum_nights",
        "has_availability",
        "availability_30",
        "availability_60",
        "availability_90",
        "availability_365",
        "number_of_reviews",
        "number_of_reviews_ltm",
        "number_of_reviews_l30d",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
        "instant_bookable",
        "calculated_host_listings_count",
        "calculated_host_listings_count_entire_homes",
        "calculated_host_listings_count_private_rooms",
        "calculated_host_listings_count_shared_rooms",
        "reviews_per_month",
    ]

    # Dodaj brakujące kolumny z wartością NaN
    for col in desired_columns:
        if col not in df.columns:
            df[col] = pd.NA

    # Zatrzymaj tylko kolumny z listy i w odpowiedniej kolejności
    return df[desired_columns]

def process_calendar_csv(df):
    desired_columns = [
        "listing_id",
        "date",
        "available",
        "price",
        "minimum_nights",
        "maximum_nights",
    ]

    for col in desired_columns:
        if col not in df.columns:
            df[col] = pd.NA

    return df[desired_columns]

def process_reviews_csv(df):
    desired_columns = [
        "listing_id",
        "id",
        "date",
        "reviewer_id",
        "reviewer_name",
    ]

    for col in desired_columns:
        if col not in df.columns:
            df[col] = pd.NA

    return df[desired_columns]


def fetch_airbnb_data():
    DB_DIR = os.path.join(DOWNLOAD_DIR, "DB")
    NEW_DIR = os.path.join(DOWNLOAD_DIR, "NEW")
    UPDATE_DIR = os.path.join(DOWNLOAD_DIR, "UPDATE")
    
    for folder in [DB_DIR, NEW_DIR, UPDATE_DIR]:
        os.makedirs(folder, exist_ok=True)   
    
    before_files = os.listdir(DB_DIR)
    before_count = len(before_files) - 1

    existing_files = {}
    for fname in before_files:
        if not fname.endswith(".csv") and not fname.endswith(".geojson"):
            continue
        base_key, file_date = extract_base_and_date(fname)
        if base_key not in existing_files or file_date > existing_files[base_key][0]:
            existing_files[base_key] = (file_date, fname)

    added = []
    updated = []
    unchanged = []
    skipped_empty = []


    response = requests.get(BASE_URL)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)

    ##### ONLY MAIN CITIES #####
    target_links = [
        urljoin(BASE_URL, link["href"])
        for link in links
        if link["href"].endswith((
            "listings.csv.gz",
            "calendar.csv.gz",
            "reviews.csv.gz"
        ))
        and any(city in link["href"].lower() for city in [
            #"vienna", "prague", "paris", "berlin", "rome", "lisbon", "madrid", "london"
            "rome", "madrid"
        ])
    ]

    ##### ALL CITIES #####
    # target_links = [
    #     urljoin(BASE_URL, link["href"])
    #     for link in links
    #     if link["href"].endswith((
    #         "listings.csv.gz",
    #         "calendar.csv.gz",
    #         "reviews.csv.gz"))
        
    #     # if 'chile' in link["href"] # odkomentuj, aby pobrać tylko Chile
    # ]

    print(f"Znaleziono {len(target_links)} plików do pobrania.\n")

    for url in target_links:
        new_filename = normalize_filename(url)
        base_key, new_date = extract_base_and_date(new_filename)
        
        if "ireland_ireland_ireland" in new_filename or 'china_beijing' in new_filename:
            print(f"[!] Pominięto plik: {new_filename}")
            skipped_empty.append(new_filename)
            continue

        
        destination = None

        existing = existing_files.get(base_key)
        if existing:
            old_date, old_fname = existing
            if new_date <= old_date:
                unchanged.append(new_filename)
                print(f"[=] Bez zmian: {new_filename}")
                continue
            else:
                # os.remove(os.path.join(DOWNLOAD_DIR, old_fname))
                destination = UPDATE_DIR
                print(f"[↑] Aktualizacja: {old_fname} → {new_filename}")
                updated.append(new_filename)
        else:
            added.append(new_filename)
            destination = NEW_DIR
            print(f"[+] Nowy plik: {new_filename}")

        file_path = os.path.join(destination, new_filename)

        # Pobieranie i zapis
        if url.endswith(".csv.gz"):
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with gzip.GzipFile(fileobj=r.raw) as gz_file:
                    df = pd.read_csv(gz_file)
                    
            if "listings" in new_filename:
                df = process_listings_csv(df)
            elif "calendar" in new_filename:
                df = process_calendar_csv(df)
            elif "reviews" in new_filename:
                df = process_reviews_csv(df)

            df.to_csv(file_path, index=False)
        else:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

    # Podsumowanie
    after_count_DB = len([f for f in os.listdir(DB_DIR) if f.endswith(".csv") or f.endswith(".geojson")])
    after_count_NEW = len([f for f in os.listdir(NEW_DIR) if f.endswith(".csv") or f.endswith(".geojson")])
    after_count = after_count_DB + after_count_NEW
    print("\nPodsumowanie operacji:")
    print(f"Plików przed: {before_count}")
    print(f"Plików po:    {after_count}")
    print(f"Dodano:     {len(added)}")
    print(f"Zaktualizowano: {len(updated)}")
    print(f"Pominięto: {len(skipped_empty)}")
    print(f"Bez zmian:  {len(unchanged)}")

    if updated:
        print("\nPliki zaktualizowane:")
        for f in updated:
            print(" -", f)
    
    if unchanged:
        print("\nPliki bez zmian:")
        for f in unchanged:
            print(" -", f)
    
    if skipped_empty:
        print(f"\nPominięto {len(skipped_empty)} plików:")
        for f in skipped_empty:
            print(" -", f)


if __name__ == "__main__":
    fetch_airbnb_data()
    log_file.close()

