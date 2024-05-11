
# Google Sheets Data Updater

Automate the process of updating your Google Sheets spreadsheet with Shopify data and receive notifications on Slack.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Google Sheets Setup](#google-sheets-setup)
  - [Shopify Setup](#shopify-setup)
  - [Slack Setup](#slack-setup)
  - [Script Configuration](#script-configuration)
- [Usage](#usage)
- [Scheduling with crontab](#scheduling-with-crontab)
- [Contributing](#contributing)
- [License](#license)
- [Additional Note](#additional-note)

## Features

- Fetches data from Shopify API and updates a Google Sheets spreadsheet.
- Calculates difference percentages between consecutive days' data.
- Sends notification messages to Slack after updating the spreadsheet.
- Easily customizable and extensible for different use cases.

## Prerequisites

- Python 3.x installed on your system.
- Access to the Google Cloud Console to generate service account credentials.
- Access to your Shopify store admin to obtain the store name and access token.
- Permission to create and configure a Slack app for posting messages to channels.

## Setup

### Google Sheets Setup

1. Create a Google Sheets spreadsheet to store your data.
2. Obtain the spreadsheet ID from its URL (e.g., `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`).
3. Generate a service account key file from the Google Cloud Console.
4. Share the Google Sheets spreadsheet with the email address associated with the service account.

### Shopify Setup

1. Log in to your Shopify store admin.
2. Navigate to **Apps** > **Manage private apps**.
3. Create a new private app and note down the store name and access token.

### Slack Setup

1. Create a new Slack app from the [Slack API website](https://api.slack.com/apps).
2. Install the app to your Slack workspace.
3. Note down the OAuth token and the name of the channel where you want to receive notifications.

### Script Configuration

Update the following constants in the script (`update_google_sheet.py`):

- `GOOGLE_SHEETS_SPREADSHEET_ID`: Replace with your Google Sheets spreadsheet ID.
- `GOOGLE_SHEETS_CREDS_FILE`: Replace with the path to your service account key file.
- `SHOPIFY_STORE_NAME`: Replace with your Shopify store name.
- `SHOPIFY_ACCESS_TOKEN`: Replace with your Shopify access token.
- `SLACK_TOKEN`: Replace with your Slack OAuth token.
- `SLACK_CHANNEL`: Replace with the name of the Slack channel where you want to receive notifications.

## Usage

1. Run the script using Python:

```bash
python test.py
```

2. The script will update the Google Sheets spreadsheet with data for specified dates, calculate difference percentages, and send notification messages to the specified Slack channel.

## Scheduling with crontab

To schedule the script to run automatically at specific intervals, use crontab. For example, to run the script daily at 2:00 AM:

```
0 2 * * * /usr/bin/python3 /path/to/test.py
```

Replace `/usr/bin/python3` with the path to your Python interpreter if it's different, and replace `/path/to/test.py` with the full path to your Python script.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Additional Note

1. **Data Availability on Shopify**: When attempting to fetch data from Shopify for a specific date, it was found that data was not available because the store's data was last updated up to February 2024.

2. **Order Retrieval Code**: Despite the limitations mentioned above, on querying for the date 12/10/2024, four product details with payment status "Paid" were successfully retrieved. A separate code (`order.py`) has been developed for this purpose. To reference and test this code, one needs to adjust the date in the code accordingly.

3. **Total Revenue Calculation Code**: A separate code (`revenue.py`) has been developed to calculate the total revenue or total sale for each date. On querying for the date 12/10/2024, the total revenue could be obtained as the products' total value was present in the Shopify store.

4. **Output Display**: Both the order details and the total revenue are displayed in the console log. One simply needs to adjust the dates according to the desired query.

5. **Code Repository and Collaboration**: All the relevant code has been shared on GitHub separately. Collaborative access has been provided to `admin@betterbody.co`. Additionally, access to a Google Data Sheet has been granted for tracking purposes. The link to the Google Data Sheet is provided for reference.(https://docs.google.com/spreadsheets/d/1Y0wnD4MBglbtfRnawAtwfNUJSdaK9qYBwLwvbmUxM-8/edit?usp=sharing)


 ```
