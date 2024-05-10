import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Constants for Google Sheets
GOOGLE_SHEETS_CREDS_FILE = r'D:\NFT-Project\Shopify_Script\shopify-data-script-771f98e7adc0.json'  
GOOGLE_SHEETS_SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_SHEETS_SPREADSHEET_ID = '1Y0wnD4MBglbtfRnawAtwfNUJSdaK9qYBwLwvbmUxM-8'

# Constants for Shopify
SHOPIFY_STORE_NAME = 'betterbody-co-test.myshopify.com'
SHOPIFY_ACCESS_TOKEN = "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"

# Constants for Slack
SLACK_TOKEN = 'xoxb-7043338520034-7063186473169-clq9g3OOedCwGjYNJ5MqWZoB'
SLACK_CHANNEL = '#tech-systems-engineer-maneuver'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enter_data(date):
    """Enter data for a specific date."""
    data = {}
    if date == datetime.date(2024, 5, 6):
        data[date] = {
            'sessions': 319,
            'revenue': 1745,
            'orders': 5,
            'conversion_rate': 5 / 319,  # Assuming orders / sessions for simplicity
            'aov': 1745 / 5  # Assuming revenue / orders for simplicity
        }
    elif date == datetime.date(2024, 5, 5):
        data[date] = {
            'sessions': 81,
            'revenue': 1200,
            'orders': 3,
            'conversion_rate': 3 / 81,  # Assuming orders / sessions for simplicity
            'aov': 1200 / 3  # Assuming revenue / orders for simplicity
        }
    elif date == datetime.date(2024, 4, 6):
        data[date] = {
            'sessions': 287,
            'revenue': 1500,
            'orders': 6,
            'conversion_rate': 6 / 287,  # Assuming orders / sessions for simplicity
            'aov': 1500 / 6  # Assuming revenue / orders for simplicity
        }
    return data

def calculate_difference(previous_value, current_value):
    """Calculate difference percentage."""
    if previous_value == 0:
        return None
    return ((current_value - previous_value) / previous_value) * 100

def update_google_sheet():
    """Update Google Sheet with entered data and difference percentages."""
    scope = GOOGLE_SHEETS_SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID).sheet1

    # Append headings to the Google Sheet
    headings = ['Date', 'Sessions', 'Difference %', 'Revenue', 'Difference %', 'Orders', 'Difference %', 'Conversion Rate', 'Difference %', 'AOV', 'Difference %']
    sheet.append_row(headings)

    # Enter data and difference percentages for May 6, 2024
    data = enter_data(datetime.date(2024, 5, 6))
    prev_day_sessions = 250
    prev_day_revenue = 1500
    prev_day_orders = 4
    prev_day_conversion_rate = prev_day_orders / prev_day_sessions
    prev_day_aov = prev_day_revenue / prev_day_orders if prev_day_orders != 0 else 0
    session_diff_percent = calculate_difference(prev_day_sessions, data[datetime.date(2024, 5, 6)]['sessions'])
    revenue_diff_percent = calculate_difference(prev_day_revenue, data[datetime.date(2024, 5, 6)]['revenue'])
    orders_diff_percent = calculate_difference(prev_day_orders, data[datetime.date(2024, 5, 6)]['orders'])
    conversion_rate_diff_percent = calculate_difference(prev_day_conversion_rate, data[datetime.date(2024, 5, 6)]['conversion_rate'])
    aov_diff_percent = calculate_difference(prev_day_aov, data[datetime.date(2024, 5, 6)]['aov'])
    row = [
        '2024-05-06',
        data[datetime.date(2024, 5, 6)]['sessions'],
        session_diff_percent,
        data[datetime.date(2024, 5, 6)]['revenue'],
        revenue_diff_percent,
        data[datetime.date(2024, 5, 6)]['orders'],
        orders_diff_percent,
        data[datetime.date(2024, 5, 6)]['conversion_rate'],
        conversion_rate_diff_percent,
        data[datetime.date(2024, 5, 6)]['aov'],
        aov_diff_percent
    ]
    sheet.append_row(row)

    
    data = enter_data(datetime.date(2024, 5, 5))
    prev_day_sessions = 200
    prev_day_revenue = 1300
    prev_day_orders = 3
    prev_day_conversion_rate = prev_day_orders / prev_day_sessions
    prev_day_aov = prev_day_revenue / prev_day_orders if prev_day_orders != 0 else 0
    session_diff_percent = calculate_difference(prev_day_sessions, data[datetime.date(2024, 5, 5)]['sessions'])
    revenue_diff_percent = calculate_difference(prev_day_revenue, data[datetime.date(2024, 5, 5)]['revenue'])
    orders_diff_percent = calculate_difference(prev_day_orders, data[datetime.date(2024, 5, 5)]['orders'])
    conversion_rate_diff_percent = calculate_difference(prev_day_conversion_rate, data[datetime.date(2024, 5, 5)]['conversion_rate'])
    aov_diff_percent = calculate_difference(prev_day_aov, data[datetime.date(2024, 5, 5)]['aov'])
    row = [
        '2024-05-05',
        data[datetime.date(2024, 5, 5)]['sessions'],
        session_diff_percent,
        data[datetime.date(2024, 5, 5)]['revenue'],
        revenue_diff_percent,
        data[datetime.date(2024, 5, 5)]['orders'],
        orders_diff_percent,
        data[datetime.date(2024, 5, 5)]['conversion_rate'],
        conversion_rate_diff_percent,
        data[datetime.date(2024, 5, 5)]['aov'],
        aov_diff_percent
    ]
    sheet.append_row(row)

    # Enter data and difference percentages for April 6, 2024
    data = enter_data(datetime.date(2024, 4, 6))
    prev_day_sessions = 200
    prev_day_revenue = 1300
    prev_day_orders = 3
    prev_day_conversion_rate = prev_day_orders / prev_day_sessions
    prev_day_aov = prev_day_revenue / prev_day_orders if prev_day_orders != 0 else 0
    session_diff_percent = calculate_difference(prev_day_sessions, data[datetime.date(2024, 4, 6)]['sessions'])
    revenue_diff_percent = calculate_difference(prev_day_revenue, data[datetime.date(2024, 4, 6)]['revenue'])
    orders_diff_percent = calculate_difference(prev_day_orders, data[datetime.date(2024, 4, 6)]['orders'])
    conversion_rate_diff_percent = calculate_difference(prev_day_conversion_rate, data[datetime.date(2024, 4, 6)]['conversion_rate'])
    aov_diff_percent = calculate_difference(prev_day_aov, data[datetime.date(2024, 4, 6)]['aov'])
    row = [
        '2024-04-06',
        data[datetime.date(2024, 4, 6)]['sessions'],
        session_diff_percent,
        data[datetime.date(2024, 4, 6)]['revenue'],
        revenue_diff_percent,
        data[datetime.date(2024, 4, 6)]['orders'],
        orders_diff_percent,
        data[datetime.date(2024, 4, 6)]['conversion_rate'],
        conversion_rate_diff_percent,
        data[datetime.date(2024, 4, 6)]['aov'],
        aov_diff_percent
    ]
    sheet.append_row(row)

    # Send a message to Slack
    send_slack_message("Google Sheet updated successfully.")

    logger.info("Google Sheet updated successfully.")

def send_slack_message(message):
    """Send message to Slack."""
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logger.info("Message sent to Slack.")
    except SlackApiError as e:
        logger.error(f"Error sending message to Slack: {e.response['error']}")

def main():
    """Main function to update Google Sheet."""
    update_google_sheet()

if __name__ == "__main__":
    main()

