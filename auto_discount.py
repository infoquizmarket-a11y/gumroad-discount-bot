import requests
import random
import string
import os

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']

def generate_discount_code(product_name):
    # Create unique prefix based on product name
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_all_products_discount_codes():
    url = "https://api.gumroad.com/v2/products"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get list of all products
        response = requests.get(url, headers=headers)
        print(f"Products API Response: {response.status_code}")
        
        if response.status_code == 200:
            products = response.json().get('products', [])
            print(f"Found {len(products)} products")
            
            success_count = 0
            total_products = len(products)
            
            # Update discount code for EVERY product
            for product in products:
                product_id = product['id']
                product_name = product['name']
                product_permalink = product.get('permalink', 'N/A')
                
                print(f"\n--- Updating: {product_name} ---")
                print(f"Product ID: {product_id}")
                print(f"Permalink: {product_permalink}")
                
                # Generate unique discount code for this product
                new_code = generate_discount_code(product_name)
                
                # Update the discount code
                update_url = f"https://api.gumroad.com/v2/products/{product_id}"
                update_data = {
                    "discount_code": new_code
                }
                
                update_response = requests.put(update_url, headers=headers, json=update_data)
                print(f"Update Response: {update_response.status_code}")
                
                if update_response.status_code == 200:
                    print(f"✅ Success! Discount code updated to: {new_code}")
                    success_count += 1
                else:
                    print(f"❌ Failed: {update_response.text}")
                
                # Small delay to avoid rate limiting
                import time
                time.sleep(1)
            
            # Final summary
            print(f"\n🎉 SUMMARY: Updated {success_count} out of {total_products} products successfully!")
            return success_count == total_products
            
        else:
            print(f"❌ Failed to fetch products: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    update_all_products_discount_codes()
