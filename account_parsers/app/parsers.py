import os
from typing import Any

from playwright.sync_api import ElementHandle, Page, sync_playwright

from app.utils import load_cookies, save_cookies


class BaseParser:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.cookies_path = f'cookies/cookies_{bank_name}.json'

    def load_env_variables(self):
        return self

    def login(self, page):
        raise NotImplementedError("Subclasses should implement this method")

    def go_to_transactions(self, page):
        raise NotImplementedError("Subclasses should implement this method")

    def get_transactions(self, page: Page):
        raise NotImplementedError("Subclasses should implement this method")

    def parse(self):
        self.load_env_variables()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()

            # Load cookies if they exist
            try:
                load_cookies(context, self.cookies_path)
            except FileNotFoundError:
                pass

            page = context.new_page()
            self.login(page)

            # Save cookies after login
            save_cookies(context, self.cookies_path)

            self.go_to_transactions(page)
            transactions = self.get_transactions(page)

            browser.close()
            return transactions


class DeutscheBankParser(BaseParser):
    def __init__(self):
        super().__init__('DB')

    def load_env_variables(self):
        self.branch = os.getenv(f'{self.bank_name}_BRANCH')
        self.account = os.getenv(f'{self.bank_name}_ACCOUNT')
        self.subaccount = os.getenv(f'{self.bank_name}_SUBACCOUNT')
        self.pin = os.getenv(f'{self.bank_name}_PIN')

    def login(self, page):
        # Go to the login page
        page.goto("https://meine.deutsche-bank.de/trxm/db/init.do")

        # Wait for the cookie popup and handle it
        try:
            page.wait_for_selector('[data-testid="uc-deny-all-button"]', timeout=5000)  # Wait up to 5 seconds for the popup
            page.click('[data-testid="uc-deny-all-button"]')  # Click the deny button
        except:
            pass  # If the popup doesn't appear, continue

        # Fill in the login details
        page.fill('input[name="branch"]', self.branch)
        page.fill('input[name="account"]', self.account)
        page.fill('input[name="subaccount"]', self.subaccount)
        page.fill('input[name="pin"]', self.pin)

        # Click the submit button
        page.click('input[type="submit"]')

    def go_to_transactions(self, page):
        # Click the link containing the text "Transactions"
        page.click('a:has-text("Transactions")')
        page.wait_for_load_state()

    def _parse_transaction_header(self, row: ElementHandle) -> dict[str, Any]:
        transaction = {}
        transaction['date'] = row.query_selector('td.date span').text_content().strip()
        transaction['value_date'] = row.query_selector('td.date:not(:first-child)').text_content().strip()
        transaction['purpose'] = row.query_selector('td.purpose').text_content().strip()
        transaction['debit'] = row.query_selector('td.balance.debit').text_content().replace('Direct Debit return', '').strip() or None
        transaction['credit'] = row.query_selector('td.balance.credit').text_content().strip() or None
        transaction['currency'] = row.query_selector('td[headers="bTcurrency"]').text_content().strip()
        return transaction

    def _parse_transaction_details(self, row: ElementHandle) -> dict[str, Any]:
        details = {}
        detail_rows = row.query_selector_all('tr')
        for detail_row in detail_rows:
            cells = detail_row.query_selector_all('td')
            if len(cells) >= 2:
                key = cells[0].text_content().strip()
                value = cells[1].text_content().strip()
                details[key] = value
        return details

    def get_transactions(self, page: Page):
        selector = '#contentContainer > table > tbody > tr.odd, #contentContainer > table > tbody > tr.even'
        rows = page.query_selector_all(selector)

        transactions = []
        is_details = False

        for _, row in enumerate(rows):
            if not is_details:
                transaction = self._parse_transaction_header(row)
                transactions.append(transaction)
                is_details = 'hasSEPADetails' in row.get_attribute('class')
            else:
                details = self._parse_transaction_details(row)
                transaction = transactions[-1]
                transaction['details'] = details
                is_details = False

        return transactions


class RevolutParser(BaseParser):
    def __init__(self):
        super().__init__('REVOLUT')

    def login(self, page):
        # Implement Revolut login
        pass

    def go_to_transactions(self, page):
        # Implement navigation to transactions for Revolut
        pass

    def get_transactions(self, page):
        # Implement transaction extraction for Revolut
        return ['revolut placeholder']


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    db_parser = DeutscheBankParser()

    print(db_parser.parse())
