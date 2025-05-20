import os
import sys
from datetime import datetime

UPDATE_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\UPDATE"
DB_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\DB"

# Ustawienie logowania do pliku
today_str = datetime.today().strftime('%Y%m%d%H%M%S')
log_path = fr"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\logs\2 remove_from_DB\remove_from_DB_{today_str}.txt"
log_file = open(log_path, mode="w", encoding="utf-8")

# Przekierowanie stdout i stderr do pliku
sys.stdout = log_file
sys.stderr = log_file

def get_key(filename):
    # usuwa datę (format YYYYMMDD_) z początku nazwy pliku
    return "_".join(filename.split("_")[1:])

def remove_db_files_with_update_keys(update_dir, db_dir):
    update_files = [f for f in os.listdir(update_dir) if os.path.isfile(os.path.join(update_dir, f)) and f != ".gitkeep"]
    print(f"Znaleziono {len(update_files)} plików w folderze UPDATE.")

    # zbierz klucze plików z UPDATE
    update_keys = set(get_key(f) for f in update_files)

    removed_files = []

    # sprawdź pliki w DB
    db_files = [f for f in os.listdir(db_dir) if os.path.isfile(os.path.join(db_dir, f)) and f != ".gitkeep"]
    for db_file in db_files:
        db_key = get_key(db_file)
        if db_key in update_keys:
            db_file_path = os.path.join(db_dir, db_file)
            os.remove(db_file_path)
            removed_files.append(db_file)
            print(f"Usunięto plik z DB: {db_file}")

    print(f"\nPodsumowanie:")
    print(f"Plików w UPDATE: {len(update_files)}")
    print(f"Plików w DB przed usuwaniem: {len(db_files)}")
    print(f"Usunięto plików w DB: {len(removed_files)}")
    print(f"Plików w DB po usuwaniu: {len(db_files) - len(removed_files)}")

if __name__ == "__main__":
    remove_db_files_with_update_keys(UPDATE_DIR, DB_DIR)
