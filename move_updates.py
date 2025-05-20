import os
import shutil
import sys
from datetime import datetime

INPUT_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\UPDATE"
OUTPUT_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\NEW"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ustawienie logowania do pliku
today_str = datetime.today().strftime('%Y%m%d%H%M%S')
log_path = fr"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\logs\3 move_updates\move_updates_{today_str}.txt"
log_file = open(log_path, mode="w", encoding="utf-8")

# Przekierowanie stdout i stderr do pliku
sys.stdout = log_file
sys.stderr = log_file


input_files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f)) and f != ".gitkeep"]
output_files_before = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]

print(f"Plików w UPDATE przed przeniesieniem: {len(input_files)}")
print(f"Plików w NEW przed przeniesieniem: {len(output_files_before)}")

moved_files = []
for filename in input_files:
    src_path = os.path.join(INPUT_DIR, filename)
    dst_path = os.path.join(OUTPUT_DIR, filename)
    shutil.move(src_path, dst_path)
    moved_files.append(filename)
    print(f"Przeniesiono: {filename}")

output_files_after = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]

print("\nPodsumowanie:")
print(f"Przeniesiono plików: {len(moved_files)}")
print(f"Plików w NEW po przeniesieniu: {len(output_files_after)}")
print("Lista przeniesionych plików:")
for f in moved_files:
    print(" -", f)