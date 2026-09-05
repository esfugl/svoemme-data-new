from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Definer parametre præcist efter DMI EDR standarden
# Vi tilføjer 'parameter-name' for eksplicit at fortælle, hvad vi vil have (f.eks. temperatur)
url = "https://dmi.dk"
params = {
    "coords": "POINT(12.635 55.655)",        # Amager Strand (Længdegrad Breddegrad)
    "datetime": dato_streng,                  # I morgen kl. 08:00 dansk tid
    "parameter-name": "temperature-2m",      # Henter specifikt lufttemperaturen i 2 meters højde
    "f": "json"                               # Gennemtvinger JSON format
}

headers = {
    "Accept": "application/json"
}

print(f"Forbinder til DMI Frie Data...")
print(f"Forespørger på dato (UTC): {dato_streng}")

try:
    # 3. Lav API-kaldet
    response = requests.get(url, params=params, headers=headers)
    
    print(f"Server svarede med statuskode: {response.status_code}")
    response.raise_for_status()

    # Tjek om svaret faktisk indeholder noget data, før vi dekoder det
    if not response.text.strip():
        print("Fejl: Serveren sendte et tomt svar tilbage (0 bytes). Tjek om tidspunktet er tilgængeligt i prognosen.")
    else:
        # 4. Fortolk JSON data
        data = response.json()
        print("\n=== VEJRPROGNOSE FOR AMAGER STRAND ER MODTAGET ===")
        print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Fejl: {http_err}")
    if response.text:
        print(f"Server svar: {response.text[:200]}")
except json.JSONDecodeError:
    print("Fejl: Kunne ikke læse svaret som JSON. Serveren sendte i stedet følgende rå tekst:")
    print(response.text[:500])  # Udskriver rådata så vi kan se fejlen (f.eks. hvis det er binært data)
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
