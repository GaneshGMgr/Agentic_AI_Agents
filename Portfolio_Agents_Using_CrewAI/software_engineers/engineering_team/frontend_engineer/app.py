Here's a simple Gradio UI that demonstrates the given backend class in `portfolio_managements.py`. Save this code as `app.py` and run it alongside your backend module. The UI provides functionalities for account creation, deposits, withdrawals, share buying/selling, portfolio value calculation, profit/loss reporting, and transaction history.

```python
import gradio as gr
from portfolio_managements import Portfolio, get_share_price

def create_ui():
    with gr.Blocks() as demo:
        account = gr.State(value={"balance": 1000})
        deposits = gr.State(value=[])
        withdrawals = gr.State(value=[])
        holdings = gr.State(value={})
        profit_loss = gr.State(value=0)
        transactions = gr.State(value=[])

        account_form = gr.inputs.Textbox(lines=1, label="Initial Deposit", placeholder="Enter deposit amount")
        create_account_btn = gr.buttons.Button(value="Create Account", variant="primary")
        deposit_form = gr.inputs.Number(min_value=0, label="Deposit Amount", step=100)
        deposit_btn = gr.buttons.Button(value="Deposit", variant="primary")
        withdraw_form = gr.inputs.Number(min_value=0, label="Withdraw Amount", step=100)
        withdraw_btn = gr.buttons.Button(value="Withdraw", variant="primary")
        buy_stocks_form = gr.inputs.Textbox(lines=2, label="Stock Symbols & Quantities (e.g., AAPL 5, TSLA 3)", placeholder="Enter stock symbols and quantities separated by spaces")
        buy_stocks_btn = gr.buttons.Button(value="Buy Stocks", variant="primary")
        sell_stocks_form = gr.inputs.Textbox(lines=2, label="Stock Symbols & Quantities (e.g., AAPL 5, TSLA 3)", placeholder="Enter stock symbols and quantities separated by spaces")
        sell_stocks_btn = gr.buttons.Button(value="Sell Stocks", variant="primary")

        portfolio_value = gr.Textbox(label="Portfolio Value: $0", visible=False)
        profit_loss_text = gr.Textbox(label="Profit/Loss: $0", visible=False)
        transaction_history = gr.DataTable(headers=["Type", "Amount", "Time"], visible=False)

        demo.queue(update_account)(account, deposits, withdrawals, holdings, profit_loss, transactions)
        demo.queue(update_ui)(portfolio_value, profit_loss_text, transaction_history)

        demo.interface.set_images(['/static/assets/img/gradio-logo-light.png'])
        demo.launch(title="Trading Simulation", functional_view=True, inline=True)

def update_account(account, deposits, withdrawals, holdings, profit_loss, transactions, new_account, deposit_amount, withdrawal_amount, stocks_buy, stocks_sell):
    if new_account:
        portfolio = Portfolio()
        portfolio.create_account(new_account["balance"])
        account.set_value({"balance": portfolio.account_balance})
        deposits.set_value(deposits)
        withdrawals.set_value(withdrawals)
        holdings.set_value(portfolio.holdings)
        profit_loss.set_value(profit_loss)
        transactions.set_value(transactions + [{"Type": "Account Created", "Time": str(portfolio.transaction_history[-1][0])}])

    if deposit_amount:
        portfolio = Portfolio(account["balance"])
        portfolio.deposit(deposit_amount)
        account.set_value({"balance": portfolio.account_balance})
        deposits.set_value(deposits + [portfolio.transaction_history[-1]])
        profit_loss.set_value(profit_loss)

    if withdrawal_amount:
        portfolio = Portfolio(account["balance"])
        portfolio.withdraw(withdrawal_amount)
        account.set_value({"balance": portfolio.account_balance})
        withdrawals.set_value(withdrawals + [portfolio.transaction_history[-1]])
        profit_loss.set_value(profit_loss)

    if stocks_buy:
        symbols_quantities = list(map(lambda x: x.split(), stocks_buy.strip().split(";")))
        portfolio = Portfolio(account["balance"])
        for symbol, quantity in symbols_quantities:
            try:
                shares_to_buy = int(quantity / get_share_price(symbol)) if symbol != "GOOGL" else int(quantity / 2700.0)
                portfolio.buy_stocks(symbol, shares_to_buy)
            except Exception as e:
                print(f"Error buying {symbol}: {e}")
        account.set_value({"balance": portfolio.account_balance})
        holdings.set_value(portfolio.holdings)
        transactions.set_value(transactions + [portfolio.transaction_history[-1]])
        profit_loss.set_value(profit_loss)

    if stocks_sell:
        symbols_quantities = list(map(lambda x: x.split(), stocks_sell.strip().split(";")))
        portfolio = Portfolio(account["balance"])
        for symbol, quantity in symbols_quantities:
            try:
                shares_to_sell = int(quantity) if symbol != "GOOGL" else 2
                if shares_to_sell > portfolio.holdings[symbol]:
                    print(f"Error selling {symbol}: Not enough shares owned")
                else:
                    portfolio.sell_stocks(symbol, shares_to_sell)
            except Exception as e:
                print(f"Error selling {symbol}: {e}")
        account.set_value({"balance": portfolio.account_balance})
        holdings.set_value(portfolio.holdings)
        transactions.set_value(transactions + [portfolio.transaction_history[-1]])
        profit_loss.set_value(profit_loss)

def update_ui(portfolio_value, profit_loss_text, transaction_history, account):
    portfolio_value.update(f"Portfolio Value: ${account['balance']}")
    profit_loss_text.update(f"Profit/Loss: $ {profit_loss.get_value()}")
    transaction_history.rows = list(map(lambda x: [x["Type"], str(x["Amount"]), x["Time"]], transactions))

if __name__ == "__main__":
    create_ui()
```