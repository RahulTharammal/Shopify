import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Constants for Shopify API, Google Sheets, and Slack
SHOPIFY_STORE_NAME = 'betterbody-co-test.myshopify.com'
SHOPIFY_ACCESS_TOKEN = "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"
SHOPIFY_API_URL = f"https://{SHOPIFY_STORE_NAME}/admin/api/2023-04/reports.json"
GOOGLE_SHEETS_CREDS_FILE = r'D:\NFT-Project\Shopify_Script\shopify-data-script-771f98e7adc0.json'  
GOOGLE_SHEETS_SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_SHEETS_SPREADSHEET_ID = '1Y0wnD4MBglbtfRnawAtwfNUJSdaK9qYBwLwvbmUxM-8'
SLACK_TOKEN = 'xoxb-7043338520034-7063186473169-clq9g3OOedCwGjYNJ5MqWZoB'
SLACK_CHANNEL = '#tech-systems-engineer-maneuver'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_shopify_data(dates):
    """Fetch data from Shopify reports for given dates."""
    headers = {
        'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN,
        'Content-Type': 'application/json',
    }
    all_data = []
    for date in dates:
        params = {
            'date': date.strftime('%Y-%m-%d'),
        }
        try:
            response = requests.get(SHOPIFY_API_URL, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for any HTTP error
            data = response.json().get('results', {})
            logger.info(f"Shopify data fetched successfully for {date}.")
            all_data.append(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from Shopify: {e}")
            all_data.append({})
    return all_data

def calculate_percent_difference(current_value, previous_value):
    """Calculate percent difference between current and previous values."""
    try:
        current_value = float(current_value)
        previous_value = float(previous_value)
        if previous_value == 0:
            return 0
        return ((current_value - previous_value) / previous_value) * 100
    except (ValueError, TypeError):
        return None  # Return None if values cannot be converted to float or are None

def update_google_sheet(data):
    """Update Google Sheet with fetched data."""
    scope = GOOGLE_SHEETS_SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID).sheet1

    # Prepare data for updating the sheet
    header = ["Date", "Sessions", "Difference % ", "Revenue", "Difference % ", 
              "Orders", "Difference % ", "Conversion Rate", "Difference % ",
              "Average Order Value", "Difference % "]
    rows_to_update = [header]
    
    # Define session values for each date
    session_values = [319, 81, 287]  # Example session values for each date

    for i, day_data in enumerate(data):
        current_date = datetime.date(2024, 5, 6) - datetime.timedelta(days=i)
        previous_date = current_date - datetime.timedelta(days=1)
        previous_month_date = current_date.replace(year=current_date.year - int(current_date.month == 1), 
                                                    month=current_date.month - 1 if current_date.month > 1 else 12)
        
        current_sessions = session_values[i] if i < len(session_values) else 'N/A'
        current_revenue = day_data.get('revenue', 'N/A') if 'revenue' in day_data else 'N/A'
        current_orders = day_data.get('orders', 'N/A') if 'orders' in day_data else 'N/A'
        current_conversion_rate = day_data.get('conversion_rate', 'N/A') if 'conversion_rate' in day_data else 'N/A'
        current_average_order_value = day_data.get('average_order_value', 'N/A') if 'average_order_value' in day_data else 'N/A'

        # Fetch previous day data
        previous_day_data = data[i + 1] if i + 1 < len(data) else {}
        previous_day_sessions = session_values[i + 1] if i + 1 < len(session_values) else 'N/A'
        previous_day_revenue = previous_day_data.get('revenue', 'N/A') if 'revenue' in previous_day_data else 'N/A'
        previous_day_orders = previous_day_data.get('orders', 'N/A') if 'orders' in previous_day_data else 'N/A'
        previous_day_conversion_rate = previous_day_data.get('conversion_rate', 'N/A') if 'conversion_rate' in previous_day_data else 'N/A'
        previous_day_average_order_value = previous_day_data.get('average_order_value', 'N/A') if 'average_order_value' in previous_day_data else 'N/A'

        # Fetch previous month data
        previous_month_data = data[-30] if i >= 30 else {}
        previous_month_sessions = session_values[i - 30] if i - 30 >= 0 else 'N/A'
        previous_month_revenue = previous_month_data.get('revenue', 'N/A') if 'revenue' in previous_month_data else 'N/A'
        previous_month_orders = previous_month_data.get('orders', 'N/A') if 'orders' in previous_month_data else 'N/A'
        previous_month_conversion_rate = previous_month_data.get('conversion_rate', 'N/A') if 'conversion_rate' in previous_month_data else 'N/A'
        previous_month_average_order_value = previous_month_data.get('average_order_value', 'N/A') if 'average_order_value' in previous_month_data else 'N/A'

        sessions_diff_prev_day = calculate_percent_difference(current_sessions, previous_day_sessions)
        revenue_diff_prev_day = calculate_percent_difference(current_revenue, previous_day_revenue)
        orders_diff_prev_day = calculate_percent_difference(current_orders, previous_day_orders)
        conversion_rate_diff_prev_day = calculate_percent_difference(current_conversion_rate, previous_day_conversion_rate)
        average_order_value_diff_prev_day = calculate_percent_difference(current_average_order_value, previous_day_average_order_value)

        sessions_diff_prev_month = calculate_percent_difference(current_sessions, previous_month_sessions)
        revenue_diff_prev_month = calculate_percent_difference(current_revenue, previous_month_revenue)
        orders_diff_prev_month = calculate_percent_difference(current_orders, previous_month_orders)
        conversion_rate_diff_prev_month = calculate_percent_difference(current_conversion_rate, previous_month_conversion_rate)
        average_order_value_diff_prev_month = calculate_percent_difference(current_average_order_value, previous_month_average_order_value)

        rows_to_update.append([
            current_date.strftime('%Y-%m-%d'), current_sessions, f"{sessions_diff_prev_day:.2f}%" if sessions_diff_prev_day is not None else 'N/A',
            current_revenue, f"{revenue_diff_prev_day:.2f}%" if revenue_diff_prev_day is not None else 'N/A',
            current_orders, f"{orders_diff_prev_day:.2f}%" if orders_diff_prev_day is not None else 'N/A',
            current_conversion_rate, f"{conversion_rate_diff_prev_day:.2f}%" if conversion_rate_diff_prev_day is not None else 'N/A',
            current_average_order_value, f"{average_order_value_diff_prev_day:.2f}%" if average_order_value_diff_prev_day is not None else 'N/A',
            
        ])

    # Clear existing data in the sheet and update with new data
    sheet.clear()
    sheet.update('A1', rows_to_update)
    logger.info("Google Sheet updated successfully.")

def send_slack_notification(message):
    """Send a notification to Slack."""
    try:
        client = WebClient(token=SLACK_TOKEN)
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logger.info("Slack notification sent successfully.")
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e.response['error']}")

def main(desired_dates):
    """Main function to fetch data and update Google Sheet."""
    data = fetch_shopify_data(desired_dates)
    update_google_sheet(data)
    send_slack_notification("Shopify data has been updated successfully.")

if __name__ == "__main__":
    desired_dates = [datetime.date(2024, 5, 6), datetime.date(2024, 5, 5), datetime.date(2024, 4, 6)]  # Dates to fetch data for
    main(desired_dates)
