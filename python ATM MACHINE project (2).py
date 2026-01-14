import time

#Initial setup
balance= 50000
DAILY_LIMIT = 20000
daily_withdrawn = 0
transaction_history = []
FILE_NAME = "transaction_history.txt"
max_attempts = 3
timeout_seconds = 10
attempts = max_attempts

#Pin validation
def is_valid_pin(pin):
    allowed_digits = {'1','2','3','4','5','6','7','8','9'}
    if len(pin) != 4:
        return False
    if len(set(pin))!=4:
        return False
    for digit in pin:
        if digit not in allowed_digits:
            return False
    return True


#Receipt functions
def print_receipt(transaction_type, amount, balance):
    print("\n----- ATM RECEIPT -----")
    print("Transaction:", transaction_type)
    print("Amount: ₦", amount)
    print("Balance: ₦", balance)
    print("--------------------\n")

def save_to_file(record):
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(record + "\n")

def read_file_history():
    try:
        with open(FILE_NAME, "r") as file:
            data = file.read()
            if data.strip() == "":
                print("No transaction history found.")
            else:
                print("\nSaved Transaction History:")
                print(data)
    except FileNotFoundError:
        print("No transaction history file found.")
    

#PIN entry
while attempts > 0:
    pin = input('Enter your 4-digit Pin(digits 1-9, no repeats): ')
    if is_valid_pin(pin):
        print("PIN accepted. Welcome.")
        print(f"\nHello, Welcome")
        break
    else:
        attempts -=1
        print(f"Invalid PIN. Attempts left:{attempts}")
       
if attempts == 0:
    print(f"\nToo many failed attempts. Please wait {timeout_seconds} seconds...")
    time.sleep(timeout_seconds)
    print("Card blocked.")
    exit()

#Menu  
while True:
    print("\nWelcome to G5 Bank ATM")
    print("1. Check Balance")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. View Transaction History")
    print("5. View Saved File History")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        print("Your balance is: ", balance)

    elif choice == "2":
        try:
            amount = int(input("Enter amount to withdraw: "))
        except ValueError:
            print('Invalid input. Please enter a number.')
            continue
        
        if 0< amount <= balance:
            balance -= amount
            record = f"Withdrew ₦{amount} | Balance: ₦{balance}"
            transaction_history.append(record)
            save_to_file(record)
            print_receipt("Withdrawal", amount, balance)
        else:
            print("Invalid amount.")

        
    elif choice == "3":
        try:
            amount = int(input("Enter amount to deposit: "))
        except ValueError:
            print('Invalid input. Please enter a number.')
            continue
        
        if amount > 0:
            balance += amount
            record = f"Deposited ₦{amount} | Balance: ₦{balance}"
            transaction_history.append(record)
            save_to_file(record)
            print_receipt("Deposit", amount, balance)
           
        
            
    elif choice == "4":
        if not transaction_history:
            print("No transactions yet.")
        else:
            for t in transaction_history:
                print("-", t)
                   
    elif choice == "5":
        read_file_history()

    elif choice == "6":
        print("Thank you for using our ATM.")
        break
       
    else:
        print("Invalid option. Try again.")
