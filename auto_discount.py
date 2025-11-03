import requests
import random
import string
import os
import time

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']

def generate_discount_code():
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_all_products_discount_codes():
    # Gumroad API endpoint for products
    url = "https://api.gumroad.com/v2/products"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Gumroad-Discount-Bot/1.0"
    }
    
    try:
        # Get list of all products
        print("📦 Fetching all products...")
        response = requests.get(url, headers=headers)
        print(f"Products API Response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"🎯 Found {len(products)} products")
            
            success_count = 0
            total_products = len(products)
            
            if total_products == 0:
                print("❌ No products found in your account")
                return False
            
            # Update discount code for EVERY product
            for index, product in enumerate(products, 1):
                product_id = product['id']
                product_name = product['name']
                product_permalink = product.get('permalink', 'N/A')
                
                print(f"\n🔄 [{index}/{total_products}] Updating: {product_name}")
                print(f"   ID: {product_id}")
                print(f"   URL: https://gumroad.com/l/{product_permalink}")
                
                # Generate unique discount code
                new_code = generate_discount_code()
                print(f"   New Code: {new_code}")
                
                # Update the product using the CORRECT API format
                update_url = f"https://api.gumroad.com/v2/products/{product_id}"
                
                # CORRECT data format for Gumroad API
                update_data = {
                    "product": {
                        "discount_code": new_code
                    }
                }
                
                # Make the update request
                update_response = requests.put(
                    update_url, 
                    headers=headers, 
                    json=update_data
                )
                
                print(f"   API Response: {update_response.status_code}")
                
                if update_response.status_code == 200:
                    print(f"   ✅ SUCCESS! Updated discount code to: {new_code}")
                    success_count += 1
                else:
                    print(f"   ❌ FAILED: {update_response.text[:200]}...")
                
                # Delay between requests to avoid rate limiting
                if index < total_products:
                    time.sleep(2)
            
            # Final summary
            print(f"\n🎉 FINAL SUMMARY")
            print(f"   Updated: {success_count}/{total_products} products")
            print(f"   Success Rate: {(success_count/total_products)*100:.1f}%")
            
            return success_count > 0
            
        else:
            print(f"❌ Failed to fetch products. Status: {response.status_code}")
            print(f"   Error: {response.text[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gumroad Discount Code Automation...")
    success = update_all_products_discount_codes()
    if success:
        print("✨ Automation completed successfully!")
    else:
        print("💥 Automation completed with errors!")
