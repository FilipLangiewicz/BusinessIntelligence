import os
import shutil
import sys
from datetime import datetime

INPUT_DIR = r"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\airbnb_data\NEW"
OUTPUT_DIR = r"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\airbnb_data\DB"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ustawienie logowania do pliku
today_str = datetime.today().strftime('%Y%m%d%H%M%S')
log_path = fr"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\logs\4 move_new\move_new_{today_str}.txt"
log_file = open(log_path, mode="w", encoding="utf-8")

# Przekierowanie stdout i stderr do pliku
sys.stdout = log_file
sys.stderr = log_file


input_files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f)) and f != ".gitkeep"]
output_files_before = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f)) and f != ".gitkeep"]

print(f"Plików w NEW przed przeniesieniem: {len(input_files)}")
print(f"Plików w DB przed przeniesieniem: {len(output_files_before)}")

moved_files = []
for filename in input_files:
    src_path = os.path.join(INPUT_DIR, filename)
    dst_path = os.path.join(OUTPUT_DIR, filename)
    shutil.move(src_path, dst_path)
    moved_files.append(filename)
    print(f"Przeniesiono: {filename}")

output_files_after = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f)) and f != ".gitkeep"]

print("\nPodsumowanie:")
print(f"Przeniesiono plików: {len(moved_files)}")
print(f"Plików w DB po przeniesieniu: {len(output_files_after)}")
print("Lista przeniesionych plików:")
for f in moved_files:
    print(" -", f)