from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Vi bygger URL'en manuelt som en rå streng for at forhindre, 
# at requests-biblioteket ændrer parenteser og mellemrum til %28 og +
base_url = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position"
full_url = f"{base_url}?coords=POINT(12.635 55.655)&datetime={dato_streng}&parameter-name=temperature-2m"

headers = {
    "Accept": "application/json",
    "User-Agent": "GitHubActions-DMI-WeatherFetch/1.0"
}

print("Forbinder til DMI Frie Data API...")
print(f"Henter vejrdata via URL: {full_url}")

try:
    # 3. Lav API-kaldet uden brug af params-dictionary for at bevare rå tekst
    response = requests.get(full_url, headers=headers)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # 4. Fortolk JSON-dataen
    data = response.json()
    print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    print(f"Serverens rå svar var: {response.text}")
except json.JSONDecodeError:
    print("Fejl: Kunne ikke fortolke svaret som JSON-struktur.")
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
