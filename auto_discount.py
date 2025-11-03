import requests
import random
import string
import os

# Get API token from GitHub Secrets - CORRECT SYNTAX
API_TOKEN = os.environ['GUMROAD_TOKEN']
PRODUCT_ID = "V0IdCdamJ6MCGYiS4lOF1g=="

def generate_discount_code():
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_gumroad_discount():
    new_code = generate_discount_code()
    
    url = f"https://api.gumroad.com/v2/products/{PRODUCT_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "product": {
            "discount_code": new_code
        }
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"✅ Success! Discount code updated to: {new_code}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    update_gumroad_discount()
