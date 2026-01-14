import time
import random

# INITIAL SETUP
DAILY_LIMIT = 20000
max_attempts = 3
timeout_seconds = 10

accounts = {}   
current_account = None


# PIN VALIDATION
def is_valid_pin(pin):
    allowed_digits = {'1','2','3','4','5','6','7','8','9'}
    if len(pin) != 4:
        return False
    if len(set(pin)) != 4:
        return False
    for digit in pin:
        if digit not in allowed_digits:
            return False
    return True


# RECEIPT
def print_receipt(transaction_type, amount, balance):
    print("\n----- ATM RECEIPT -----")
    print("Transaction:", transaction_type)
    print("Amount: ₦", amount)
    print("Balance: ₦", balance)
    print("--------------------\n")


# ACCOUNT CREATION
def create_account():
    name = input("Enter your name: ")

    while True:
        pin = input("Create a PIN (4 digits, 1-9, no repeats): ")
        if is_valid_pin(pin):
            break
        print("Invalid PIN format.")

    account_number = str(random.randint(10**9, 10**10 - 1))

    accounts[account_number] = {
        "name": name,
        "pin": pin,
        "balance": 0,
        "transaction_history": []
    }

    print("\nAccount created successfully!")
    print("Your Account Number is:", account_number)
    print("PLEASE KEEP IT SAFE.\n")


# LOGIN
def login():
    global current_account
    attempts = max_attempts

    acc_no = input("Enter Account Number: ")

    if acc_no not in accounts:
        print("Account not found.")
        return False

    while attempts > 0:
        pin = input("Enter PIN: ")
        if pin == accounts[acc_no]["pin"]:
            current_account = accounts[acc_no]
            print(f"\nWelcome {current_account['name']}!")
            return True
        else:
            attempts -= 1
            print(f"Wrong PIN. Attempts left: {attempts}")

    print(f"Too many attempts. Waiting {timeout_seconds} seconds...")
    time.sleep(timeout_seconds)
    return False


# CONFIRM PIN FOR TRANSACTIONS
def confirm_pin():
    pin = input("Re-enter your PIN to confirm: ")
    return pin == current_account["pin"]


# EDIT ACCOUNT FEATURE
def edit_account():
    # PIN verification first
    attempts_left = max_attempts
    while attempts_left > 0:
        attempt_pin = input('Enter your PIN to edit account: ')
        if attempt_pin == current_account['pin']:
            break
        else:
            attempts_left -= 1
            print(f"Invalid PIN. Attempts left: {attempts_left}")
    else:
        print(f"\nToo many failed attempts. Waiting {timeout_seconds} seconds...")
        time.sleep(timeout_seconds)
        print("Card blocked.")
        return

    valid_choice = False
    while not valid_choice:
        print("\nSelect which field to edit")
        print("1. Edit Name")
        print("2. Edit PIN")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            new_name = input("Enter new name: ").title()
            current_account['name'] = new_name
            print("Name updated successfully!")
            valid_choice = True

        elif choice == "2":
            while True:
                new_pin = input("Enter new 4-digit PIN (1-9, no repeats): ")
                if is_valid_pin(new_pin):
                    current_account['pin'] = new_pin
                    print("PIN updated successfully!")
                    break
                else:
                    print("Invalid PIN. Try again.")
            valid_choice = True

        elif choice == "3":
            break

        else:
            print("Invalid option. Try again.")


# MAIN PROGRAM LOOP
while True:

    # LOGIN / CREATE MENU
    while current_account is None:
        print("\n=== G5 BANK ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        first_choice = input("Choose an option: ")

        if first_choice == "1":
            create_account()

        elif first_choice == "2":
            login()

        elif first_choice == "3":
            exit()

        else:
            print("Invalid option.")


    # ATM MENU
    while current_account is not None:
        print(f"\nWelcome to G5 Bank ATM, {current_account['name']}")
        print("1. Check Balance")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. View Transaction History")
        print("5. Edit Account")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("Your balance is: ₦", current_account["balance"])

        elif choice == "2":
            try:
                amount = int(input("Enter amount to withdraw: "))
            except ValueError:
                print("Invalid input.")
                continue

            if not confirm_pin():
                print("Invalid PIN.")
                continue

            if 0 < amount <= current_account["balance"]:
                current_account["balance"] -= amount
                current_account["transaction_history"].append(f"Withdrew ₦{amount}")
                print_receipt("Withdrawal", amount, current_account["balance"])
            else:
                print("Invalid amount.")

        elif choice == "3":
            try:
                amount = int(input("Enter amount to deposit: "))
            except ValueError:
                print("Invalid input.")
                continue

            if not confirm_pin():
                print("Invalid PIN.")
                continue

            if amount > 0:
                current_account["balance"] += amount
                current_account["transaction_history"].append(f"Deposited ₦{amount}")
                print_receipt("Deposit", amount, current_account["balance"])
            else:
                print("Invalid amount.")

        elif choice == "4":
            if not current_account["transaction_history"]:
                print("No transactions yet.")
            else:
                for t in current_account["transaction_history"]:
                    print("-", t)

        elif choice == "5":
            edit_account()

        elif choice == "6":
            print("Logging out...")
            current_account = None

        else:
            print("Invalid option.")
