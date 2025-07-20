import os
import warnings
import logging

from software_engineers.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

# Create output directory if it doesn't exist
os.makedirs('engineering_team', exist_ok=True)
os.makedirs('engineering_team/backend_engineer', exist_ok=True)
os.makedirs('engineering_team/frontend_engineer', exist_ok=True)
os.makedirs('engineering_team/test_engineer', exist_ok=True)
os.makedirs('engineering_team/lead_engineer', exist_ok=True)

requirements = """
Create a trading simulation account system allowing account creation, deposits, and withdrawals.
Track share buys/sells with quantities.
Calculate portfolio value and profit/loss from initial deposit.
Report holdings, profit/loss, and transaction history anytime.
Prevent negative balance withdrawals, overspending on shares, and selling shares not owned.
Use get_share_price(symbol) returning fixed prices for AAPL, TSLA, GOOGL.
"""
module_name = "portfolio_managements.py"
class_name = "Portfolio"

# requirements = """
# Design and implement a simple to-do list web application. It should have a user-friendly frontend, a backend that handles adding and deleting tasks, and use local storage or a database.
# """
# module_name = "todo_app.py"
# class_name = "ToDoApp"

def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }

    # inputs = {
    # "requirements": "Create a Python module named `simple_math.py` that contains a class `SimpleMath`. The class should have one method `add(a, b)` that returns the sum of the two numbers.",
    # "module_name": "simple_math.py",
    # "class_name": "SimpleMath"
    # }
    # print("🧠 Inputs:")
    # for key, value in inputs.items():
    #     print(f"  {key}: {value}")

    print("\n🚀 Let's work the engineering team...")

    try:
        crew_instance = EngineeringTeam().crew()
        result = crew_instance.kickoff(inputs=inputs)

        print("\n Result:")
        print(result)
        print(" Crew completed successfully!")
    except Exception as e:
        print(f" An error occurred: {e}")

if __name__ == "__main__":
    run()