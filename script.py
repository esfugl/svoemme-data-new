from datetime import datetime, timedelta
import json
import requests

# 1. Beregn automatisk datoen for i morgen kl. 08:00 dansk tid (06:00 UTC)
i_morgen = datetime.utcnow() + timedelta(days=1)
dato_streng = i_morgen.strftime("%Y-%m-%dT06:00:00Z")

# 2. Den præcise EDR API-sti til positioner jf. DMI's specifikationer
# Vi holder os strengt til formatet /position uden indlejrede koordinater i stien
url = "https://dmi.dk"

# 3. Parametrene sendes som en dictionary. Requests-biblioteket sørger selv 
# for at sammensætte query-strengen korrekt.
params = {
    "coords": "POINT(12.635 55.655)",  # Amager Strand (længdegrad breddegrad)
    "datetime": dato_streng,
    "f": "json"                         # Tvinger formatet til JSON i stedet for HTML
}

# 4. Vi tilføjer de nødvendige system-headers for at fortælle DMI, at vi er et script
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHubActions/1.0"
}

print("Forinder til DMI Frie Data API...")
print(f"Forespørger på Amager Strand for tidspunktet: {dato_streng}")

try:
    # Lav kaldet med 'allow_redirects=False' så vi fanger det med det samme, hvis den prøver at hoppe til dmi.dk forsiden
    response = requests.get(url, params=params, headers=headers, allow_redirects=False)
    
    print(f"Server svarede med HTTP-status: {response.status_code}")
    
    if response.status_code in [301, 302, 307]:
        print("Fejl: DMI forsøgte at omdirigere kaldet til TYPO3-forsiden. URL'en eller parametrene afvises.")
        print(f"Omdirigerings-adresse var: {response.headers.get('Location')}")
    else:
        response.raise_for_status()
        
        # 5. Fortolk JSON-dataen
        data = response.json()
        print("\n=== SUCCESS: VEJRDATA MODTAGET FRA DMI ===")
        print(json.dumps(data, indent=4, ensure_ascii=False))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP-Fejl opstod: {http_err}")
except json.JSONDecodeError:
    print("Fejl: Kunne ikke fortolke svaret som JSON. Svaret startede med:")
    print(response.text[:300])
except requests.exceptions.RequestException as e:
    print(f"Netværksfejl: {e}")
