import os

class Bank:
    def __init__(self, name, account_no):
        self.name = name
        self.account_no = account_no
        self.balance = 0  # Initialize balance to 0

    def display(self):
        print(f"Your account has been created successfully for {self.name}.")
        print(f"Account Number: {self.account_no}, Balance: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.log_transaction("Deposit", amount)
            print(f"${amount:.2f} has been deposited. New balance: ${self.balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.log_transaction("Withdraw", amount)
            print(f"${amount:.2f} has been withdrawn. New balance: ${self.balance:.2f}")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def log_transaction(self, transaction_type, amount):
        log_entry = f"{transaction_type}: ${amount:.2f} from account {self.account_no} for {self.name}\n"
        with open("transaction_logs.txt", "a") as log_file:
            log_file.write(log_entry)

    def transfer(self, amount, to_account):
        if 0 < amount <= self.balance:
            self.withdraw(amount)
            to_account.deposit(amount)
            self.log_transaction("Transfer", amount)
            print(f"${amount:.2f} has been transferred to account {to_account.account_no}.")
        else:
            print("Transfer amount must be positive and less than or equal to your balance.")


class CurrentAccount(Bank):
    def __init__(self, name, account_no):
        super().__init__(name, account_no)

class SavingAccount(Bank):
    def __init__(self, name, account_no):
        super().__init__(name, account_no)

# Global dictionary to store accounts
accounts = {}

def create_account():
    account_number = input("Enter account number: ")
    account_holder = input("Enter account holder name: ")

    print("\nChoose account type:")
    print("1. Savings")
    print("2. Current")
    account_type = input("Enter your choice (1 or 2): ")

    if account_type == '1':
        account = SavingAccount(account_holder, account_number)
    elif account_type == '2':
        account = CurrentAccount(account_holder, account_number)
    else:
        print("Invalid account type. Please choose '1' for savings or '2' for current.")
        return None

    # Store the account in the dictionary
    accounts[account_number] = account
    return account

def access_account():
    account_number = input("Enter your account number to access: ")

    if account_number in accounts:
        return accounts[account_number]
    else:
        print("Account does not exist. Please create a new account.")
        return None

def view_logs():
    print("\nTransaction Logs:")
    if os.path.exists("transaction_logs.txt"):
        with open("transaction_logs.txt", "r") as log_file:
            logs = log_file.readlines()
            if logs:
                for log in logs:
                    print(log.strip())
            else:
                print("No transaction logs found.")
    else:
        print("No transaction logs file found.")

def transfer_funds(from_account):
    to_account_number = input("Enter the account number to transfer to: ")

    if to_account_number in accounts:
        to_account = accounts[to_account_number]
        amount = float(input("Enter amount to transfer: "))
        from_account.transfer(amount, to_account)
    else:
        print("The account number to transfer to does not exist.")

def main():
    while True:
        print("\nWelcome to the Bank")
        print("1. Create a new account")
        print("2. Access an existing account")
        print("3. View transaction logs")
        print("4. Exit")
        choice = input("Choose an option (1, 2, 3, or 4): ")

        if choice == '1':
            new_account = create_account()
            if new_account:
                new_account.display()
        elif choice == '2':
            existing_account = access_account()
            if existing_account:
                existing_account.display()

                # Example usage of deposit, withdraw, and transfer
                while True:
                    print("\nChoose an action:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer Funds")
                    print("4. Exit to main menu")
                    action = input("Enter your choice (1, 2, 3, or 4): ")

                    if action == '1':
                        amount = float(input("Enter amount to deposit: "))
                        existing_account.deposit(amount)
                    elif action == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        existing_account.withdraw(amount)
                    elif action == '3':
                        transfer_funds(existing_account)
                    elif action == '4':
                        print("Exiting to main menu.")
                        break
                    else:
                        print("Invalid action. Please choose '1', '2', '3', or '4'.")
        elif choice == '3':
            view_logs()
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please choose '1', '2', '3', or '4'.")

# Run the main function
main()
