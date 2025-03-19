import requests
import pandas as pd
import time
import os

url = "https://api.squaresigns.com/api/Shopping/Calculate"

min_size = 4
max_width = 48
max_height = 96
default_count = 2 

product_id = 1343

headers = {
    "Content-Type": "application/json"
}

print("Script started.")
print(f"URL: {url}")
print(f"Product ID: {product_id}")
print(f"Width range: {min_size} to {max_width}")
print(f"Height range: {min_size} to {max_height}")
print(f"Default count: {default_count}")
print("-" * 40)

file_exists = os.path.isfile("size_price_combinations.csv")

for width in range(min_size, max_width + 1):
    data = []

    print(f"Processing width: {width}...")

    for height in range(min_size, max_height + 1):
       
        print(f"  Processing height: {height}...")

        payload = {
            "productId": product_id,
            "width": width,
            "height": height,
            "count": default_count
        }

        print(f"    Payload: {payload}")

        try:
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  

            print(f"    Request successful. Status code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                
                print(f"    Response: {result}")

                price = result.get("price")
                old_price = result.get("oldPrice")
                discounted_each_stock_price = result.get("discountedEachStockPrice")
                each_stock_price = result.get("eachStockPrice")

                data.append({
                    "Width": width,
                    "Height": height,
                    "Quantity": default_count,
                    "Price": price,
                    "Old Price": old_price,
                    "Discounted Each Stock Price": discounted_each_stock_price,
                    "Each Stock Price": each_stock_price
                })
            else:
                
                print(f"    Failed to fetch data for {width}x{height}. Status code: {response.status_code}")
                print(f"    Response: {response.text}")

        except requests.exceptions.RequestException as e:
            
            print(f"    Request failed: {e}")

    
    if data:
        df = pd.DataFrame(data)
        df.to_csv("size_price_combinations.csv", mode="a", index=False, header=not file_exists)
        print(f"  Data for width {width} saved to size_price_combinations.csv")
        file_exists = True  
    else:
        print(f"  No data to save for width {width}.")

    time.sleep(2)

print("Script completed.")

