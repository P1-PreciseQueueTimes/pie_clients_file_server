import requests

mac_adress = "fa:10:b5:f2:ff:51" 

resp = requests.get(f"https://www.macvendorlookup.com/api/v2/{mac_adress}/json")

company = resp.json()[0]["company"]

print(company)
