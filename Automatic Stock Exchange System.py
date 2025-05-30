import os
import re

# Constants for file paths
ACCOUNT_FILE = "accounts4.txt"
EXECUTION_LOG_FILE = "execution_log4.txt"

# Input Validation Class
class InputValidator:
    @staticmethod
    def is_input_empty(prompt_msg):
        while True:
            value = input(prompt_msg).strip()
            if value:
                return value
            print("Input cannot be empty. Please try again.")

    @staticmethod
    def is_number_positive(prompt_msg):
        while True:
            try:
                value = float(input(prompt_msg))
                if value > 0:
                    return value
                else:
                    print("The value must be greater than zero. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_stock_name(stock_name):
        if not stock_name.isalnum():
            print("Invalid stock name. It should only contain letters and numbers.")
            return False
        return True

    @staticmethod
    def validate_amount(amount):
        if not amount.isdigit() or int(amount) <= 0:
            print("Invalid amount. Please enter a positive whole number.")
            return False
        return True

    @staticmethod
    def validate_user_id(user_id, accounts):
        return any(account.user_id == int(user_id) for account in accounts)


# Account Class
class Account:
    id_counter = 1  # Class-level attribute to keep track of IDs

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = Account.id_counter

    def __str__(self):
        return f"ID: {self.user_id}, Name: {self.first_name} {self.last_name}, Email: {self.email}"

# List to load all the accounts created
accounts = []

# Account handling functions
def save_new_account_to_file(account):
    try:
        with open(ACCOUNT_FILE, "a") as file:
            file.write(f"{account.user_id},{account.first_name},{account.last_name},{account.email}\n")
    except IOError:
        print("Error saving account. Please try again.")

def load_accounts_from_file():
    global accounts
    accounts.clear()  # Ensure accounts list is reset
    if os.path.exists(ACCOUNT_FILE):
        try:
            with open(ACCOUNT_FILE, "r") as file:
                max_id = 0
                for line in file:
                    user_id, first_name, last_name, email = line.strip().split(",")
                    account = Account(first_name, last_name, email)
                    account.user_id = int(user_id)
                    accounts.append(account)
                    max_id = max(max_id, account.user_id)
                Account.id_counter = max_id + 1  # Set counter to the next available ID
        except IOError:
            print("Error loading accounts file. Please check the file.")

def create_account():
    print("\n--- Create an Account ---")
    first_name = InputValidator.is_input_empty("Enter your first name: ")
    last_name = InputValidator.is_input_empty("Enter your last name: ")

    while True:
        email = InputValidator.is_input_empty("Enter your email address: ")
        if InputValidator.is_valid_email(email):
            break
        print("Invalid email format. Please try again.")

    # Create a new account instance
    new_account = Account(first_name, last_name, email)
    
    # Increment the Account.id_counter for the next account
    Account.id_counter += 1
    
    # Add the account to the accounts list
    accounts.append(new_account)  
    
    # Save only the new account to the file
    save_new_account_to_file(new_account)  

    print(f"Account created successfully! Your User ID is {new_account.user_id}.")
    print(new_account)


# Stock Classes
class Bidding:
    def __init__(self, stock_name, bidding_price, amount, user_id):
        self.stock_name = stock_name
        self.bidding_price = bidding_price
        self.amount = amount
        self.user_id = user_id

    def __str__(self):
        return f"Bidding -> Stock: {self.stock_name}, Price: {self.bidding_price}, Amount: {self.amount}, User ID: {self.user_id}"

class Asking:
    def __init__(self, stock_name, asking_price, amount, user_id):
        self.stock_name = stock_name
        self.asking_price = asking_price
        self.amount = amount
        self.user_id = user_id

    def __str__(self):
        return f"Asking -> Stock: {self.stock_name}, Price: {self.asking_price}, Amount: {self.amount}, User ID: {self.user_id}"

# Transaction lists
biddings = []
askings = []

# Transaction handling functions
def add_bidding():
    print("\n--- Make a Bidding ---")
    stock_name = InputValidator.is_input_empty("Enter stock name: ").strip().lower()
    if not InputValidator.validate_stock_name(stock_name):
        return
    bidding_price = InputValidator.is_number_positive("Enter your bidding price: ")
    amount = InputValidator.is_input_empty("Enter the number of stocks: ").strip()
    if not InputValidator.validate_amount(amount):
        return
    amount = int(amount)
    user_id = InputValidator.is_input_empty("Enter your User ID: ")

    if not InputValidator.validate_user_id(user_id, accounts):
        print("Invalid User ID. Please create an account first.")
        return

    new_bid = Bidding(stock_name, bidding_price, amount, user_id)
    biddings.append(new_bid)
    print("Bidding placed successfully!")
    match_bid_and_ask()

def add_asking():
    print("\n--- Make an Asking ---")
    stock_name = InputValidator.is_input_empty("Enter stock name: ").strip().lower()
    if not InputValidator.validate_stock_name(stock_name):
        return
    asking_price = InputValidator.is_number_positive("Enter your asking price: ")
    amount = InputValidator.is_input_empty("Enter the number of stocks: ").strip()
    if not InputValidator.validate_amount(amount):
        return
    amount = int(amount)
    user_id = InputValidator.is_input_empty("Enter your User ID: ")

    if not InputValidator.validate_user_id(user_id, accounts):
        print("Invalid User ID. Please create an account first.")
        return

    new_ask = Asking(stock_name, asking_price, amount, user_id)
    askings.append(new_ask)
    print("Asking placed successfully!")
    match_bid_and_ask()

def sort_biddings():
    biddings.sort(key=lambda x: x.bidding_price, reverse=True)

def sort_askings():
    askings.sort(key=lambda x: x.asking_price)

def match_bid_and_ask():
    global biddings, askings

    sort_biddings()
    sort_askings()

    matched = []
    for bid in biddings:
        for ask in askings:
            if bid.user_id == ask.user_id:
                continue

            if bid.stock_name == ask.stock_name and bid.bidding_price >= ask.asking_price:
                matched.append((bid, ask))

    for bid, ask in matched:
        execute_match(bid, ask)

def execute_match(bid, ask):
    number_of_orders = min(bid.amount, ask.amount)
    print(f"{number_of_orders} order(s) successfully executed at {ask.asking_price}.")

    execution_log(bid.stock_name, number_of_orders, ask.asking_price, bid.user_id, ask.user_id)

    bid.amount -= number_of_orders
    ask.amount -= number_of_orders

    if bid.amount == 0:
        biddings.remove(bid)
    if ask.amount == 0:
        askings.remove(ask)

def execution_log(stock_name, number_of_orders, execution_price, bid_user_id, ask_user_id):
    try:
        with open(EXECUTION_LOG_FILE, "a") as file:
            file.write(f"Stock: {stock_name}, Orders: {number_of_orders}, Price: {execution_price}, "
                       f"Bidding User ID: {bid_user_id}, Asking User ID: {ask_user_id}\n")
    except IOError:
        print("Error logging the transaction.")

# Main Menu Class
class MainMenu:
    @staticmethod
    def display_menu():
        while True:
            print("\n--- Automated Stock Exchange System ---")
            print("1. Create an Account")
            print("2. Make a Bidding")
            print("3. Make an Asking")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                create_account()
            elif choice == '2':
                add_bidding()
            elif choice == '3':
                add_asking()
            elif choice == '4':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a valid option.")


# Program entry point
if __name__ == "__main__":
    load_accounts_from_file()
    MainMenu.display_menu()
