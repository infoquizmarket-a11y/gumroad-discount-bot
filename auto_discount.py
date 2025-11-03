import requests
import random
import string
import os
import time

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']

def test_api_connection():
    """Test if our API token is working"""
    print("🔍 Testing API connection...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple GET request to products
    test_url = "https://api.gumroad.com/v2/products"
    response = requests.get(test_url, headers=headers)
    
    print(f"📡 API Test Response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"✅ API Connection SUCCESSFUL!")
        print(f"📊 Found {len(products)} products")
        
        for product in products:
            print(f"   - {product['name']} (ID: {product['id']})")
        
        return True, products
    else:
        print(f"❌ API Connection FAILED: {response.status_code}")
        print(f"   Error: {response.text[:200]}")
        return False, []

def generate_discount_code():
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_product_discount(product_id, product_name):
    """Update discount code for a single product"""
    new_code = generate_discount_code()
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Try the CORRECT Gumroad API v2 format
    update_url = f"https://api.gumroad.com/v2/products/{product_id}"
    
    # Multiple data format attempts
    data_formats = [
        {"discount_code": new_code},
        {"product": {"discount_code": new_code}},
        {"offer_code": new_code},
        {"product": {"offer_code": new_code}}
    ]
    
    print(f"   Testing {len(data_formats)} different data formats...")
    
    for i, data in enumerate(data_formats, 1):
        print(f"   Format {i}: {data}")
        
        try:
            response = requests.put(update_url, headers=headers, json=data)
            print(f"      Response: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS with format {i}! Code: {new_code}")
                return True
            else:
                print(f"      Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"      Exception: {e}")
        
        time.sleep(1)
    
    print(f"   ❌ All formats failed for {product_name}")
    return False

def main():
    print("🚀 Starting Gumroad Discount Code Automation...")
    
    # First test API connection
    success, products = test_api_connection()
    
    if not success:
        print("💥 Cannot proceed - API connection failed")
        return False
    
    if not products:
        print("💥 No products found")
        return False
    
    print(f"\n🔄 Starting to update {len(products)} products...")
    
    success_count = 0
    for product in products:
        product_id = product['id']
        product_name = product['name']
        
        print(f"\n📦 Updating: {product_name}")
        print(f"   ID: {product_id}")
        
        if update_product_discount(product_id, product_name):
            success_count += 1
        
        time.sleep(2)  # Rate limiting
    
    print(f"\n🎉 FINAL RESULTS:")
    print(f"   Successfully updated: {success_count}/{len(products)} products")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    if success:
        print("✨ Automation completed successfully!")
    else:
        print("💥 Automation completed with errors!")
