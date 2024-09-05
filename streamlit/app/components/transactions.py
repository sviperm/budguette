style = """
    <style>
        :root {
            --date-section-bg: #F0F2F6;
            --transaction-bg: #FFFFFF;
            --red-text-color: #FF4B4B;
            --green-text-color: #228B22;
        }
        .transactions-container {
            font-family: 'Arial', sans-serif;
            padding: 10px;
            border-radius: 10px;
            margin: 0 auto;
        }
        .transaction {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background-color: var(--transaction-bg);
            margin-bottom: 5px;
            // box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .transaction:first-child {
            border-radius: 8px 8px 0px 0px;
        }
        .transaction:last-child {
            border-radius: 0px 0px 8px 8px;
        }
        .transaction:first-child:last-child {
            border-radius: 8px;
        }
        .transaction:not(:last-child) {
            margin-bottom: 3px;
        }
        .transaction-info {
            display: flex;
            flex-direction: column;
        }
        .transaction-name {
            font-weight: bold;
        }
        .transaction-time {
            color: grey;
            font-size: 0.9em;
        }
        .transaction-amount {
            text-align: right;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .transaction-category {
            color: grey;
            font-size: 0.9em;
        }
        .date-section {
            margin-bottom: 20px;
            padding: 10px;
            background-color: var(--date-section-bg);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        .date-header {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0px 5px
        }
        .total-amount {
            font-size: 1em;
            font-weight: normal;
        }
    </style>
"""


class TransactionComponent:
    def __init__(self, name, datetime, amount, currency, category):
        self.name = name
        self.datetime = datetime
        self.amount = amount
        self.currency = currency
        self.category = category

    def render(self):
        amount_color = 'var(--green-text-color)' if self.amount > 0 else 'var(--red-text-color)'
        html = f"""
        <div class="transaction">
            <div class="transaction-info">
                <div class="transaction-name">{self.name}</div>
                <div class="transaction-time">{self.datetime.strftime('%H:%M')}</div>
            </div>
            <div class="transaction-amount" style="color: {amount_color};">
                <div>{self.currency}{self.amount:.2f}</div>
                <div class="transaction-category">{self.category}</div>
            </div>
        </div>
        """
        return html


class DateComponent:
    def __init__(self, date, transactions):
        self.date = date
        self.transactions = transactions
        self.total_amount = sum(transaction.amount for transaction in transactions)

    def render(self):
        transactions_html = ''.join([transaction.render() for transaction in self.transactions])
        total_amount_color = 'var(--green-text-color)' if self.total_amount > 0 else 'var(--red-text-color)'
        html = f"""
        <div class="date-section">
            <div class="date-header">
                <span class="date">{self.date.strftime('%b %d')}</span>
                <span class="total-amount" style="color: {total_amount_color};">
                    {self.total_amount:.2f}
                </span>
            </div>
            <div class="transactions">
                {transactions_html}
            </div>
        </div>
        """
        return html


class TransactionsContainer:
    def __init__(self, transactions):
        self.transactions = transactions

    def render(self):
        # Group transactions by date
        transactions_by_date = {}
        for transaction in self.transactions:
            date = transaction.datetime.date()
            if date not in transactions_by_date:
                transactions_by_date[date] = []
            transactions_by_date[date].append(transaction)

        date_components = [
            DateComponent(date, transactions).render()
            for date, transactions in sorted(transactions_by_date.items(), reverse=True)
        ]

        html = f"""
        {style}
        <div class="transactions-container">
            {''.join(date_components)}
        </div>
        """
        return html
