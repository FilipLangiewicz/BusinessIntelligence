import gzip
import shutil
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse

BASE_URL = "http://insideairbnb.com/get-the-data/"
DOWNLOAD_DIR = "airbnb_data"
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


def fetch_airbnb_data():
    before_files = os.listdir(DOWNLOAD_DIR)
    before_count = len(before_files)

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

    response = requests.get(BASE_URL)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)
    target_links = [
        urljoin(BASE_URL, link["href"])
        for link in links
        if link["href"].endswith((
            "listings.csv.gz",
            "calendar.csv.gz",
            "reviews.csv.gz",
            "neighbourhoods.geojson"))
    ]

    print(f"Znaleziono {len(target_links)} plików do pobrania.\n")

    for url in target_links:
        new_filename = normalize_filename(url)
        file_path = os.path.join(DOWNLOAD_DIR, new_filename)
        base_key, new_date = extract_base_and_date(new_filename)

        existing = existing_files.get(base_key)
        if existing:
            old_date, old_fname = existing
            if new_date <= old_date:
                unchanged.append(new_filename)
                print(f"[=] Bez zmian: {new_filename}")
                continue
            else:
                os.remove(os.path.join(DOWNLOAD_DIR, old_fname))
                print(f"[↑] Aktualizacja: {old_fname} → {new_filename}")
                updated.append(new_filename)
        else:
            added.append(new_filename)
            print(f"[+] Nowy plik: {new_filename}")

        # Pobieranie i zapis
        if url.endswith(".csv.gz"):
            csv_path = file_path
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with gzip.GzipFile(fileobj=r.raw) as gz_file:
                    with open(csv_path, "wb") as out_file:
                        shutil.copyfileobj(gz_file, out_file)
        else:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

    # Podsumowanie
    after_count = len([f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".csv") or f.endswith(".geojson")])
    print("\nPodsumowanie operacji:")
    print(f"Plików przed: {before_count}")
    print(f"Plików po:    {after_count}")
    print(f"Dodano:     {len(added)}")
    print(f"Zaktualizowano: {len(updated)}")
    print(f"Bez zmian:  {len(unchanged)}")

    if updated:
        print("\nPliki zaktualizowane:")
        for f in updated:
            print(" -", f)
    if unchanged:
        print("\nPliki bez zmian:")
        for f in unchanged:
            print(" -", f)


if __name__ == "__main__":
    fetch_airbnb_data()
