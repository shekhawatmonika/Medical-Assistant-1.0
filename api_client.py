import requests

def search_fda(drug_name):
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f'openfda.brand_name:"{drug_name}"', "limit": 3}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return {"message": "No public API result was returned."}
        data = response.json()
        return [
            {
                "brand_name": item.get("openfda", {}).get("brand_name", []),
                "manufacturer": item.get("openfda", {}).get("manufacturer_name", []),
            }
            for item in data.get("results", [])
        ]
    except requests.RequestException as exc:
        return {"error": str(exc)}
