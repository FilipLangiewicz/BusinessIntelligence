from weatherapi.rest import ApiException
from datetime import datetime, timedelta, date
import os
import re
import weatherapi
import sys
import csv
from API_KEY import get_API_KEY

today_str = datetime.today().strftime('%Y%m%d%H%M%S')

# 🔒 Ścieżka do logów
log_path = fr"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\logs\5 weather_api\weather_api_{today_str}.txt"
log_file = open(log_path, mode="w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

# 🔧 Konfiguracja API
configuration = weatherapi.Configuration()
configuration.api_key['key'] = get_API_KEY()
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

# 📁 Folder z plikami CSV (miasta) i zapisem wyników
DB_DIR = r"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\airbnb_data\DB"
WEATHER_DIR = r"C:\Users\natal\Desktop\STUDIA\SEM_6\hurtownie\projekt\BusinessIntelligence\airbnb_data\WEATHER"
os.makedirs(WEATHER_DIR, exist_ok=True)

# 🔁 Ustaw ścieżkę do pliku CSV i usuń poprzedni, jeśli istnieje
weather_csv_path = os.path.join(WEATHER_DIR, "weather.csv")
if os.path.exists(weather_csv_path):
    os.remove(weather_csv_path)

# 📝 Zapisz nagłówki nowego pliku CSV
with open(weather_csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "weather_id", "date", "location_name", "avg_temp", "max_temp", "min_temp",
        "daily_will_it_rain", "daily_will_it_snow", "daily_chance_of_rain",
        "daily_chance_of_snow", "sunrise", "sunset", "last_modified_date"
    ])

# 📦 Funkcja pobierająca pogodę i zapisująca do CSV
def save_weather_to_csv(city, date_str):
    dt = datetime.strptime(date_str, "%Y%m%d").date()
    dt_api = dt.strftime("%Y-%m-%d")
    response = api_instance.future_weather(q=city, dt=dt_api, lang="pl")
    forecast_day = response['forecast']['forecastday'][0]
    day = forecast_day['day']
    astro = forecast_day['astro']
    hours = forecast_day['hour']

    will_rain = "YES" if any(h['will_it_rain'] for h in hours) else "NO"
    will_snow = "YES" if any(h['will_it_snow'] for h in hours) else "NO"
    chance_rain = max(h['chance_of_rain'] for h in hours)
    chance_snow = max(h['chance_of_snow'] for h in hours)

    weather_id = f"{city.replace('-', '').lower()}{date_str}"
    location_name = response['location']['name']
    sunrise = datetime.strptime(astro['sunrise'], "%I:%M %p").time()
    sunset = datetime.strptime(astro['sunset'], "%I:%M %p").time()

    today = date.today()

    row = [
        weather_id, dt, location_name, day['avgtemp_c'], day['maxtemp_c'], day['mintemp_c'],
        will_rain, will_snow, chance_rain, chance_snow, sunrise, sunset, today
    ]

    with open(weather_csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row)

# 📋 Wyodrębnij unikalne miasta z plików CSV
cities = set()
for file in os.listdir(DB_DIR):
    parts = file.split("_")
    if len(parts) >= 4 and file.endswith("listings.csv"):
        city = parts[3].lower()
        cities.add(city)

# 🗓 Zakres dat
today = datetime.today().date()
start_date = today + timedelta(days=14)
end_date = today + timedelta(days=300)

# 🔁 Pobierz dane pogodowe
for city in cities:
    successful_dates = []
    skip_city = False
    for i in range((end_date - start_date).days + 1):
        if skip_city:
            break

        date_obj = start_date + timedelta(days=i)
        date_str = date_obj.strftime("%Y%m%d")
        try:
            save_weather_to_csv(city, date_str)
            successful_dates.append(date_str)
        except ApiException as e:
            if e.status == 400 or "No matching location found" in str(e):
                print(f"❌ Lokalizacja **{city}** jest nieprawidłowa — pomijam dalsze próby.")
                skip_city = True
                break
            else:
                print(f"⚠️ Błąd API przy {city} ({date_str}): {e}")
        except Exception as e:
            print(f"⚠️ Błąd ogólny przy {city} ({date_str}): {e}")

    if successful_dates:
        print(f"✅ Pobrano dane pogodowe dla miasta **{city}** dla {len(successful_dates)} dni.")
    elif not skip_city:
        print(f"❌ Nie udało się pobrać żadnych danych pogodowych dla miasta **{city}**.")
