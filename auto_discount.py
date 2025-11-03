import requests
import random
import string
import os
import time

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']

def generate_discount_code():
    """Generate a random discount code"""
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for i in range(8))
    return random_code

def main():
    print("🚀 Starting Universal Gumroad Discount Code Automation...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Get all products
    print("📦 Fetching all products...")
    response = requests.get("https://api.gumroad.com/v2/products", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch products: {response.status_code}")
        print(f"Error: {response.text[:200]}")
        return False
    
    products = response.json().get('products', [])
    print(f"🎯 Found {len(products)} products total")
    
    if len(products) == 0:
        print("❌ No products found in your account")
        return False
    
    success_count = 0
    
    # Process ALL products regardless of name
    for index, product in enumerate(products, 1):
        product_id = product['id']
        product_name = product['name']
        product_type = product.get('product_type', 'N/A')
        
        print(f"\n🔄 [{index}/{len(products)}] Processing: {product_name}")
        print(f"   Type: {product_type}")
        print(f"   ID: {product_id}")
        
        # Generate new random discount code
        new_code = generate_discount_code()
        print(f"   New Code: {new_code}")
        
        # Update the product
        update_url = f"https://api.gumroad.com/v2/products/{product_id}"
        
        update_response = requests.put(
            update_url, 
            headers=headers, 
            json={"discount_code": new_code}
        )
        
        print(f"   API Response: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print(f"   ✅ SUCCESS! Updated discount code")
            success_count += 1
        else:
            print(f"   ❌ FAILED: {update_response.text[:150]}...")
        
        # Wait between requests to avoid rate limiting
        if index < len(products):
            time.sleep(2)
    
    # Final results
    print(f"\n🎉 UNIVERSAL AUTOMATION COMPLETE!")
    print(f"   Total Products: {len(products)}")
    print(f"   Successfully Updated: {success_count}")
    print(f"   Failed: {len(products) - success_count}")
    print(f"   Success Rate: {(success_count/len(products))*100:.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    if success:
        print("✨ All products processed successfully!")
    else:
        print("💥 Some products failed to update!")
