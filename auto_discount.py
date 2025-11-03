import requests
import random
import string
import os

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']
PRODUCT_ID = "V0IdCdamJ6MCGYiS4lOF1g=="

def generate_discount_code():
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_gumroad_discount():
    new_code = generate_discount_code()
    
    # CORRECT API ENDPOINT
    url = "https://api.gumroad.com/v2/products/ixqqw"  # Using your product permalink
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # CORRECT DATA FORMAT
    data = {
        "discount_code": new_code
    }
    
    try:
        response = requests.put(url, headers=headers, data=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Success! Discount code updated to: {new_code}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    update_gumroad_discount()
