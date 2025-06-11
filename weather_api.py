from weatherapi.rest import ApiException
from datetime import datetime, timedelta, date
import os
import re
import weatherapi
import sys
import csv
from API_KEY import get_API_KEY
from time import sleep

# wygenerowano przy użyciu ChatGPT - zwalidował Filip Langiewicz

today_str = datetime.today().strftime('%Y%m%d%H%M%S')

# 🔒 Ścieżka do logów
log_path = fr"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\logs\5 weather_api\weather_api_{today_str}.txt"
log_file = open(log_path, mode="w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

# 🔧 Konfiguracja API
configuration = weatherapi.Configuration()
configuration.api_key['key'] = get_API_KEY()
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

# 📁 Folder z plikami CSV (miasta) i zapisem wyników
DB_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\NEW"
WEATHER_DIR = r"D:\STUDIA\Semestr 6\Hurtownie danych i systemy Business Intelligence\Laboratoria\Projekt\BusinessIntelligence\airbnb_data\WEATHER"
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
days_back = 365

# 🔁 Pobierz dane pogodowe

MIN_DAY = 14
MAX_DAY = 300

# 🔁 Pobierz dane pogodowe
for city in cities:
    successful_dates = set()
    all_dates = []

    for i in range(365):
        date_obj = today + timedelta(days=i)
        date_str = date_obj.strftime("%Y%m%d")
        all_dates.append((date_obj, date_str, i))

    for date_obj, date_str, delta_days in all_dates:
        weather_id = f"{city.replace('-', '').lower()}{date_str}"
        last_modified = date.today()

        if MIN_DAY <= delta_days <= MAX_DAY:
            # Data jest w zakresie API (14..300 dni)
            try:
                save_weather_to_csv(city, date_str)
                successful_dates.add(date_str)
            except ApiException as e:
                print(f"⚠️ Błąd API przy {city} ({date_str}): {e}")
                sleep(10)
                try:
                    save_weather_to_csv(city, date_str)
                    successful_dates.add(date_str)
                except Exception as e2:
                    print(f"❌ Druga próba dla {city} ({date_str}) nie powiodła się: {e2}")
                    with open(weather_csv_path, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            weather_id,
                            date_obj,
                            city,
                            0, 0, 0, '', '', 0, 0, '00:00:00', '00:00:00',
                            last_modified
                        ])
            except Exception as e:
                print(f"⚠️ Błąd ogólny przy {city} ({date_str}): {e}")
                with open(weather_csv_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        weather_id,
                        date_obj,
                        city,
                        0, 0, 0, '', '', 0, 0, '00:00:00', '00:00:00',
                        last_modified
                    ])
        else:
            # Data poza zakresem API — od razu wpisz pusty wiersz
            with open(weather_csv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    weather_id,
                    date_obj,
                    city,
                    0, 0, 0, '', '', 0, 0, '00:00:00', '00:00:00',
                    last_modified
                ])
                
    for i in range(1, days_back + 1):
        date_obj = today - timedelta(days=i)
        date_str = date_obj.strftime("%Y%m%d")
        weather_id = f"{city.replace('-', '').lower()}{date_str}"
        last_modified = today

        with open(weather_csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                weather_id,
                date_obj,
                city,
                0, 0, 0, '', '', 0, 0, '00:00:00', '00:00:00',
                last_modified
            ])
    
    print(f"🔁 Zapisano dane pogodowe dla miasta {city} – {len(successful_dates)}/365 dni.")

