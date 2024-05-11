
import datetime
import shopify

# Set up your Shopify API credentials
shop_url = "https://betterbody-co-test.myshopify.com"
api_version = "2023-01"
private_app_password = "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"

# Create a Shopify session
session = shopify.Session(shop_url, api_version, private_app_password)
shopify.ShopifyResource.activate_session(session)

try:
    # Define the dates for which you want to retrieve sales
    dates_to_check = ["06/05/2024", "05/05/2024", "24/04/2024"]

    for date_str in dates_to_check:
        # Convert date string to datetime object
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

        # Retrieve orders for the specified date
        orders = shopify.Order.find(created_at_min=date, created_at_max=date + datetime.timedelta(days=1))

        # Initialize variables to calculate total sales for the date
        total_sales = 0

        # Loop through each order and calculate total sales
        for order in orders:
            total_sales += float(order.total_price)

        print(f"Total sales for {date_str}: {total_sales:.2f}")

finally:
    # Clear the session when you're done
    shopify.ShopifyResource.clear_session()
