import datetime
import pytz
import shopify

# Set up your Shopify API credentials
shop_url = "https://betterbody-co-test.myshopify.com"
api_version = "2023-01"
private_app_password = "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"

# Create a Shopify session
session = shopify.Session(shop_url, api_version, private_app_password)
shopify.ShopifyResource.activate_session(session)

# Define the dates for which you want to retrieve orders
dates_to_check = [
    "06/05/2024",
    "05/05/2024",
    "16/10/2023"
]

# Convert date strings to datetime objects
date_objects = [datetime.datetime.strptime(date_str, "%d/%m/%Y") for date_str in dates_to_check]

# Convert datetime objects to ISO 8601 format
iso_dates = [date_obj.strftime("%Y-%m-%dT%H:%M:%S") for date_obj in date_objects]

# Initialize a counter for the number of orders
total_orders = 0

# Retrieve orders for the specified dates
for iso_date in iso_dates:
    try:
        # Retrieve orders created on or after the specified date
        orders = shopify.Order.find(created_at_min=iso_date, limit=50)
        for order in orders:
            # Check if the order's creation date matches the specified date exactly
            if order.created_at[:10] == iso_date[:10]:
                total_orders += 1
    except Exception as e:
        print("Error occurred:", e)

# Print the total number of orders
print("Total orders for the specified dates:", total_orders)

# Clear the session when you're done
shopify.ShopifyResource.clear_session()