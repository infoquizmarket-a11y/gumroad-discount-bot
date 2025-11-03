import requests
import random
import string
import os
import base64
import json

# Your OAuth credentials from GitHub Secrets
APPLICATION_ID = os.environ['GUMROAD_APP_ID']
APPLICATION_SECRET = os.environ['GUMROAD_APP_SECRET']
ACCESS_TOKEN = os.environ['GUMROAD_ACCESS_TOKEN']

def generate_discount_code():
    """Generate a random discount code"""
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for i in range(8))
    return random_code

def get_oauth_token():
    """Get OAuth access token using client credentials"""
    print("🔑 Getting OAuth token...")
    
    # Create Basic Auth header
    credentials = f"{APPLICATION_ID}:{APPLICATION_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "scope": "edit_products"  # Request specific permissions
    }
    
    try:
        response = requests.post(
            "https://api.gumroad.com/oauth/token",
            headers=headers,
            data=data
        )
        
        print(f"OAuth Response: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ OAuth token obtained successfully!")
            return token_data['access_token']
        else:
            print(f"❌ OAuth failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ OAuth exception: {e}")
        return None

def main():
    print("🚀 Starting Gumroad OAuth Discount Code Automation...")
    
    # Try using the provided access token first
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing provided access token...")
    test_response = requests.get("https://api.gumroad.com/v2/products", headers=headers)
    
    if test_response.status_code == 200:
        print("✅ Provided access token works!")
        access_token = ACCESS_TOKEN
    else:
        print("❌ Provided access token failed, trying OAuth flow...")
        print(f"Error: {test_response.status_code} - {test_response.text[:200]}")
        
        # Try to get new token via OAuth
        access_token = get_oauth_token()
        if not access_token:
            print("💥 All authentication methods failed!")
            return False
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    # Get products
    print("📦 Fetching products...")
    products_response = requests.get("https://api.gumroad.com/v2/products", headers=headers)
    
    if products_response.status_code != 200:
        print(f"❌ Failed to fetch products: {products_response.status_code}")
        print(f"Error: {products_response.text}")
        return False
    
    products = products_response.json().get('products', [])
    print(f"🎯 Found {len(products)} products")
    
    if not products:
        print("❌ No products found")
        return False
    
    success_count = 0
    
    # Update each product
    for product in products:
        product_id = product['id']
        product_name = product['name']
        
        print(f"\n🔄 Updating: {product_name}")
        print(f"   ID: {product_id}")
        
        new_code = generate_discount_code()
        print(f"   New Code: {new_code}")
        
        # Update product using correct endpoint
        update_url = f"https://api.gumroad.com/v2/products/{product_id}"
        update_data = {
            "discount_code": new_code
        }
        
        update_response = requests.put(update_url, headers=headers, json=update_data)
        print(f"   Update Response: {update_response.status_code}")
        
        if update_response.status_code == 200:
            result = update_response.json()
            if result.get('success', False):
                print(f"   ✅ SUCCESS! Code updated to: {new_code}")
                success_count += 1
            else:
                print(f"   ❌ API returned error: {result}")
        else:
            print(f"   ❌ HTTP Error: {update_response.text[:200]}...")
    
    print(f"\n🎉 COMPLETED: {success_count}/{len(products)} products updated")
    return success_count > 0

if __name__ == "__main__":
    success = main()
    if success:
        print("✨ Automation completed successfully!")
    else:
        print("💥 Automation failed!")
