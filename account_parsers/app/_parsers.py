import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from app.utils import load_cookies, save_cookies

# Load environment variables from .env file
load_dotenv()

# Get bank account parameters from environment variables
BRANCH = os.getenv('DB_BRANCH')
ACCOUNT = os.getenv('DB_ACCOUNT')
SUBACCOUNT = os.getenv('DB_SUBACCOUNT')
PIN = os.getenv('DB_PIN')


def login(page):
    # Go to the login page
    page.goto("https://meine.deutsche-bank.de/trxm/db/init.do")

    # Wait for the cookie popup and handle it
    try:
        page.wait_for_selector('[data-testid="uc-deny-all-button"]', timeout=5000)  # Wait up to 5 seconds for the popup
        page.click('[data-testid="uc-deny-all-button"]')  # Click the deny button
    except:
        pass  # If the popup doesn't appear, continue

    # Fill in the login details
    page.fill('input[name="branch"]', BRANCH)
    page.fill('input[name="account"]', ACCOUNT)
    page.fill('input[name="subaccount"]', SUBACCOUNT)
    page.fill('input[name="pin"]', PIN)

    # Click the submit button
    page.click('input[type="submit"]')


def go_to_transactions(page):
    # Click the link containing the text "Transactions"
    page.click('a:has-text("Transactions")')


def get_transactions(page):
    # Extract transactions
    transactions = page.query_selector_all('.transaction-row-selector')  # Replace with actual selector
    for transaction in transactions:
        date = transaction.query_selector('.date-selector').text_content()  # Replace with actual selector
        description = transaction.query_selector('.description-selector').text_content()  # Replace with actual selector
        amount = transaction.query_selector('.amount-selector').text_content()  # Replace with actual selector
        print(f"Date: {date}, Description: {description}, Amount: {amount}")


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        # Load cookies if they exist
        try:
            load_cookies(context, 'cookies.json')
        except FileNotFoundError:
            pass

        page = context.new_page()
        login(page)

        # Save cookies after login
        save_cookies(context, 'cookies.json')

        go_to_transactions(page)
        # get_transactions(page)

        page.wait_for_timeout(10_000)

        browser.close()


if __name__ == "__main__":
    main()
