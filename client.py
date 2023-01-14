import socket
import json

def send_transaction(transactions: list):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    s.connect(('localhost', 8080))
    # Prepare the data to be sent
    data = {'transactions': transactions}
    data = json.dumps(data)
    # Send the data
    s.sendall(data.encode())
    # Close the socket
    s.close()

def create_wallet():
    transactions.append({'type': 'create_wallet', 'data': 'Creating Wallet'})

def add_balance(wallet: str, amount: float):
    print({'type': 'add_balance', 'data': {'wallet': wallet, 'amount': amount}})
    transactions.append({'type': 'add_balance', 'data': {'wallet': wallet, 'amount': amount*1000000}})

def subtract_balance(wallet: str, amount: float):
    transactions.append({'type': 'subtract_balance', 'data': {'wallet': wallet, 'amount': amount*1000000}})

if __name__ == "__main__":
    while True:
        transactions = []
        print("Choose a transaction: ")
        print("Create Wallet (1)")
        print("Add Balance (2)")
        print("Subtract Balance (3)")
        print("")
        transaction_choice = int(input())
        if transaction_choice == 1:
            create_wallet()
        elif transaction_choice == 2:
            print("Enter your wallet ID: ")
            print("")
            wallet_id = input()
            print("Enter amount to add: ")
            print("")
            amount = int(input())
            add_balance(wallet_id, amount)
        elif transaction_choice == 3:
            print("Enter your wallet ID: ")
            print("")
            wallet_id = input()
            print("Enter amount to subtract: ")
            print("")
            amount = int(input())
            subtract_balance(wallet_id, amount)
        elif transaction_choice == 4:
            transactions = [{'type': 'new_transaction_test', 'data': 'Separate Transaction Test'}]
        else:
            print("Please choose a listed choice.")

        send_transaction(transactions)
