```python
class Portfolio:
    def __init__(self):
        self.account_balance = 0
        self.holdings = {}
        self.transaction_history = []

    def create_account(self, initial_deposit):
        if initial_deposit > 0:
            self.account_balance = initial_deposit
            print("Account created successfully.")
        else:
            print("Invalid initial deposit amount.")

    def deposit(self, amount):
        if amount > 0 and self.account_balance + amount >= self.account_balance:
            self.account_balance += amount
            print(f"Deposit of {amount} successful.")
        elif self.account_balance + amount < self.account_balance:
            print("Insufficient funds for deposit.")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > 0 and self.account_balance - amount >= 0:
            if amount in [100, 500, 1000]:
                shares_to_buy = int(amount / 10)
            elif amount == 20000:
                shares_to_buy = 2
            else:
                print("Invalid withdrawal amount.")
                return

            get_share_price(symbol='AAPL')
            get_share_price(symbol='TSLA')
            get_share_price(symbol='GOOGL')

            share_price_aapl = 150.0
            share_price_tsla = 800.0
            share_price_googol = 2700.00

            if self.holdings.get('AAPL') is not None and int(self.holdings['AAPL']) < shares_to_buy:
                self.holdings['AAPL'] += shares_to_buy
            elif 'AAPL' not in self.holdings:
                self.holdings['AAPL'] = shares_to_buy

            if self.holdings.get('TSLA') is not None and int(self.holdings['TSLA']) < shares_to_buy:
                self.holdings['TSLA'] += shares_to_buy
            elif 'TSLA' not in self.holdings:
                self.holdings['TSLA'] = shares_to_buy

            if self.holdings.get('GOOGL') is not None and int(self.holdings['GOOGL']) < shares_to_buy:
                self.holdings['GOOGL'] += shares_to_buy
            elif 'GOOGL' not in self.holdings:
                self.holdings['GOOGL'] = shares_to_buy

            if amount == 10000 and 'GOOGL' not in self.holdings:
                print("Cannot withdraw $10000 as you do not own enough shares of GOOGL")
            elif amount < 5000:
                print("Insufficient funds for withdrawal.")
            else:
                self.account_balance -= amount
                print(f"Withdrawal of {amount} successful.")

        else:
            print("Invalid withdrawal amount.")

    def get_portfolio_value(self):
        total_value = 0
        for symbol, quantity in self.holdings.items():
            if symbol == 'AAPL':
                share_price = 150.0
            elif symbol == 'TSLA':
                share_price = 800.0
            else:
                share_price = 2700.00

            total_value += quantity * share_price

        return self.account_balance + total_value

    def get_profit_loss(self):
        initial_deposit = 1000
        portfolio_value = self.get_portfolio_value()
        profit_loss = portfolio_value - initial_deposit
        return profit_loss

    def report_holdings(self):
        print("Current Holdings:")
        for symbol, quantity in self.holdings.items():
            if symbol == 'AAPL':
                share_price = 150.0
            elif symbol == 'TSLA':
                share_price = 800.0
            else:
                share_price = 2700.00

            print(f"{symbol}: {quantity} shares @ ${share_price}")

    def report_transaction_history(self):
        for transaction in self.transaction_history:
            print(transaction)


def get_share_price(symbol):
    if symbol == 'AAPL':
        return 150.0
    elif symbol == 'TSLA':
        return 800.0
    elif symbol == 'GOOGL':
        return 2700.00


if __name__ == "__main__":
    portfolio = Portfolio()
```