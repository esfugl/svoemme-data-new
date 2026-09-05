from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Ny præcis URL-struktur, hvor koordinaterne indgår direkte i stien (EDR-standard)
# Format: .../position/POINT(længdegrad%20breddegrad)
url = "https://dmi.dk"

# 3. Parametre til filtrering af tid og format
params = {
    "datetime": dato_streng,
    "f": "json"
}

headers = {
    "Accept": "application/json"
}

print(f"Forbinder til det åbne DMI API...")
print(f"Henter data for Amager Strand til dato: {dato_streng}")

try:
    # 4. Lav API-kaldet
    response = requests.get(url, params=params, headers=headers)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # 5. Fortolk JSON data
    data = response.json()
    print("\n=== SUCCESS: VEJRPROGNOSE FOR AMAGER STRAND ER MODTAGET ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    if response.text:
        print(f"Server svar: {response.text[:200]}")
except json.JSONDecodeError:
    print("Fejl: Svaret var stadig ikke JSON. Serveren sendte i stedet:")
    print(response.text[:300])
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
