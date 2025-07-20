```
from portfolio_managements import Portfolio
import unittest

class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio()

    def test_create_account(self):
        self.portfolio.create_account(1000)
        self.assertEqual(self.portfolio.account_balance, 1000)

    def test_deposit(self):
        self.portfolio.create_account(1000)
        self.portfolio.deposit(500)
        self.assertEqual(self.portfolio.account_balance, 1500)

    def test_withdraw(self):
        self.portfolio.create_account(1000)
        self.portfolio.deposit(500)
        self.portfolio.withdraw(250)
        self.assertEqual(self.portfolio.account_balance, 1250)

    def test_report_holdings(self):
        self.portfolio.create_account(1000)
        self.portfolio.deposit(500)
        self.portfolio.withdraw(250)
        self.portfolio.report_holdings()

    def test_get_portfolio_value(self):
        self.portfolio.create_account(1000)
        self.assertEqual(self.portfolio.get_portfolio_value(), 1000)

    def test_get_profit_loss(self):
        self.portfolio.create_account(1000)
        self.assertEqual(self.portfolio.get_profit_loss(), 0)

if __name__ == '__main__':
    unittest.main()
```