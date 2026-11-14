"""Command line expense tracker (data stored in a CSV file).

The file emma_expenses.csv shipped with the project already contains a full
year of expenses, so the statistics are meaningful from the first run.
"""

import csv
import os
import math
import numpy_financial as npf
from datetime import datetime

FILENAME = "emma_expenses.csv"  # or "personnal_expenses.csv"
COLUMNS = ["date", "category", "description", "amount"]
INCOME = 2000
ANNUAL_RATE = 0.05
LOAN_YEARS = (10, 15, 20)
MAX_DEBT_RATIO = 0.35


class Expense:
    """One expense, with its values already converted to the right type.

    A CSV file only stores text, so the amount arrives as "68.72" and not as a
    number: the conversion is done once, here.
    """

    def __init__(self, date, category, description, amount):
        self.date = date  # kept as text, e.g. "05/03/2025"
        self.category = category
        self.description = description
        self.amount = float(amount)

    def to_row(self):
        """Return the expense as a list of texts, ready to be written in the CSV."""
        return [self.date, self.category, self.description, f"{self.amount:.2f}"]


def read_expenses():
    """Return the list of expenses saved in the CSV file."""
    if not os.path.exists(FILENAME):
        return []

    expenses = []

    with open(FILENAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Each row is a dictionary of texts: we turn it into an Expense.
        for row in reader:
            expense = Expense(
                row["date"], row["category"], row["description"], row["amount"]
            )
            expenses.append(expense)

    return expenses


def save_expense(expense):
    """Append one expense at the end of the CSV file."""
    file_exists = os.path.exists(FILENAME)

    with open(FILENAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # A brand-new file needs its header line first.
        if not file_exists:
            writer.writerow(COLUMNS)

        writer.writerow(expense.to_row())


def show_history():
    """Display every saved expense along with the total."""
    expenses = read_expenses()

    if not expenses:
        print("No expense saved yet, add one first.\n")
        return

    print("\n--- Expense history ---")
    header = f"{'Date':<12}{'Category':<20}{'Description':<30}{'Amount':>10}"
    print(header)

    total = 0
    for expense in expenses:
        line = (
            f"{expense.date:<12}{expense.category:<20}"
            f"{expense.description:<30}{expense.amount:>10.2f}"
        )
        print(line)
        total += expense.amount

    print(f"\nTotal: {total:.2f} EUR over {len(expenses)} expense(s).\n")


def add_expense():
    """Ask for the details of an expense and append it to the CSV file."""
    category = input("Category (e.g. groceries, transport): ").strip()
    description = input("Description: ").strip()

    # In French a comma is used for decimals, but Python needs a dot.
    answer = input("Amount in euros: ").strip().replace(",", ".")

    try:
        amount = float(answer)
    except ValueError:
        print("Invalid amount, the expense was not saved.\n")
        return

    today = datetime.now().strftime("%d/%m/%Y")
    expense = Expense(today, category, description, amount)
    save_expense(expense)

    print(f"Expense of {expense.amount:.2f} EUR saved.\n")


def show_menu():
    """Display the available choices."""
    print("\n=== Expense tracker ===")
    print("1. Show history")
    print("2. Add an expense")
    print("3. Statistics")
    print("4. Car Purchase Simulator")
    print("5. Mortgage Simulator")
    print("6. Quit")


def show_stats():
    """Display the statistics."""
    expenses = read_expenses()

    if not expenses:
        print("No expense saved yet, add one first.\n")
        return

    print("\n--- Statistics ---")
    global_expense = total_expenses(expenses)
    months = months_covered(expenses)
    total_category = totals_by_category(expenses)
    average_per_month = monthly_averages(months, total_category)

    if months == 1:
        word = "month"
    else:
        word = "months"

    print(f"\nTotal expenses: {global_expense:.2f} EUR over {months} {word}\n")
    header = f"{'Category':<20}{'Total':>10}{'Monthly avg':>20}"
    print(header)


    for category, amount in total_category.items():
        line = f"{category:<20}{amount:>10.2f}{average_per_month[category]:>20.2f}"
        print(line)


def total_expenses(expenses):
    """Calculate the total expenses saved in the CSV file."""
    global_expense = 0
    for expense in expenses:
        global_expense += expense.amount
    return global_expense


def months_covered(expenses):
    """Calculate the number of months covered by the expenses."""
    months = set()
    for expense in expenses:
        split_date = expense.date.split("/")
        month_key = f"{split_date[1]}/{split_date[2]}"
        months.add(month_key)
    months_cov = len(months)
    return months_cov


def totals_by_category(expenses):
    """Calculate the total amount of expenses by category."""
    total_category = {}
    for expense in expenses:
        if expense.category not in total_category:
            total_category[expense.category] = expense.amount
        else:
            total_category[expense.category] += expense.amount
    return total_category


def monthly_averages(months_cov, total_category):
    """Calculate the average amount of expenses by category."""
    average_per_month = {}

    for category, amount in total_category.items():
        average_per_month[category] = amount / months_cov

    return average_per_month


def average_expenses_monthly(global_expense, months_cov):
    """Calculate the average monthly amount of expenses """
    av = global_expense / months_cov
    return av


def month_savings(income, av):
    """Calculate the monthly savings"""
    savings = income - av
    if savings <= 0:
        return None
    return savings


def months_to_buy(choice_car_price,savings):
    """Calculate the months to buy an expense."""
    months_necessary_to_buy = choice_car_price / savings
    return math.ceil(months_necessary_to_buy)


def show_month_for_car():
    """Display the number of months to buy the car."""
    expenses = read_expenses()
    if not expenses:
        print("No expense saved yet, add one first.\n")
        return

    choice_car_price = input("Car price in € : ").strip().replace(",", ".")
    try:
        amount = float(choice_car_price)
        if amount <= 0 or not math.isfinite(amount):
            print("Invalid price, enter a positive number\n")
            return
    except ValueError:
        print("Invalid amount, input only numbers.\n")
        return

    month = months_covered(expenses)
    global_expense = total_expenses(expenses)
    av = average_expenses_monthly(global_expense, month)
    savings = month_savings(INCOME, av)
    if savings is None:
        print("No savings available\n")
        return
    m_necessary_to_buy = months_to_buy(amount, savings)
    print(f"You need : {m_necessary_to_buy} months to buy your dreamed car\n")


def monthly_max_capacity(expenses):
    """Calculate the maximum payment capacity."""
    global_expense = total_expenses(expenses)
    month = months_covered(expenses)
    av = average_expenses_monthly(global_expense, month)
    total_cat = totals_by_category(expenses)
    month_cat = monthly_averages(month, total_cat)
    housing = month_cat.get("housing", 0)
    savings = month_savings(INCOME, av)
    if savings is None:
        savings = 0
    total_available_for_loan = housing + savings
    ceiling = INCOME * MAX_DEBT_RATIO
    max_capacity = min(total_available_for_loan, ceiling)
    return max_capacity


def loan_capacity(max_capacity, years, annual_rate):
    """Calculate the maximum loan capacity."""
    loan_amount = -npf.pv(annual_rate/12, years*12, max_capacity)
    return loan_amount


def show_loan_available():
    """Display the maximum loan available."""
    expenses = read_expenses()
    if not expenses:
        print("No expense saved yet, add one first.\n")
        return
    max_capacity = monthly_max_capacity(expenses)

    print("\n--- Mortgage Simulator ---\n")
    print(f"Monthly payment: {max_capacity:.0f} Euros\n")
    header = f"{'Duration':<2}{'Amount':>10}"
    print(header)
    for duration in LOAN_YEARS:
        loan_amount = loan_capacity(max_capacity, duration, ANNUAL_RATE)
        print(f"{duration:<2} years{loan_amount:>10,.0f} Euros")


def main():
    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_history()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            show_month_for_car()
        elif choice == "5":
            show_loan_available()
        elif choice == "6":
            print("See you soon!")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 6.\n")


if __name__ == "__main__":
    main()