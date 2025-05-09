import requests
from datetime import datetime

# Twoje dane wejściowe
API_KEY = "TWOJ_API_KEY"
latitude = 52.2297  # np. Warszawa
longitude = 21.0122
date = "2024-12-15"  # data w formacie YYYY-MM-DD
timezone = "Europe/Warsaw"

# Budowanie URL-a
url = (
    "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    f"?lat={latitude}&lon={longitude}&date={date}&tz={timezone}&appid={API_KEY}"
)

# Wysłanie zapytania
response = requests.get(url)

# Obsługa odpowiedzi
if response.status_code == 200:
    data = response.json()
    print(f"📅 Pogoda dla {date}:")
    print(f"🌡️ Temperatura (min): {data['temperature']['min']['value']} {data['temperature']['min']['unit']}")
    print(f"🌡️ Temperatura (max): {data['temperature']['max']['value']} {data['temperature']['max']['unit']}")
    print(f"💧 Wilgotność: {data['humidity']['mean']['value']} {data['humidity']['mean']['unit']}")
    print(f"🌦️ Warunki: {data['weather']['description']}")
else:
    print(f"❌ Błąd: {response.status_code} – {response.text}")
