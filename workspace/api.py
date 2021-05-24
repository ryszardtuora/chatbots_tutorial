import requests
import json

address = "https://corona.lmao.ninja/v2/countries/Poland?yesterday=true&strict=true&query "
response = requests.get(address)
data = json.loads(response.content)

print(f"Yesterday {data['todayCases']} people got sick, and {data['todayDeaths']} people died because of the coronavirus pandemic")
