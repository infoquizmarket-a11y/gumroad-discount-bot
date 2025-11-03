import requests
import random
import string
import os

# Get API token from GitHub Secrets
API_TOKEN = os.environ['GUMROAD_TOKEN']

def generate_discount_code():
    prefix = "JEEPHYSICS_"
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for i in range(6))
    return prefix + random_part

def update_gumroad_discount():
    new_code = generate_discount_code()
    
    # CORRECT API ENDPOINT - List products first to get the right ID
    url = "https://api.gumroad.com/v2/products"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # First, get list of products to find the correct one
        response = requests.get(url, headers=headers)
        print(f"Products API Response: {response.status_code}")
        
        if response.status_code == 200:
            products = response.json().get('products', [])
            print(f"Found {len(products)} products")
            
            # Find your JEE Physics product
            target_product = None
            for product in products:
                print(f"Product: {product.get('name')} - ID: {product.get('id')}")
                if "JEE Physics" in product.get('name', ''):
                    target_product = product
                    break
            
            if target_product:
                product_id = target_product['id']
                print(f"Updating product: {target_product['name']} (ID: {product_id})")
                
                # Now update the discount code
                update_url = f"https://api.gumroad.com/v2/products/{product_id}"
                update_data = {
                    "discount_code": new_code
                }
                
                update_response = requests.put(update_url, headers=headers, json=update_data)
                print(f"Update Response: {update_response.status_code}")
                print(f"Update Response Text: {update_response.text}")
                
                if update_response.status_code == 200:
                    print(f"✅ Success! Discount code updated to: {new_code}")
                    return True
                else:
                    print(f"❌ Update failed: {update_response.text}")
                    return False
            else:
                print("❌ JEE Physics product not found in your products")
                return False
        else:
            print(f"❌ Failed to fetch products: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    update_gumroad_discount()
