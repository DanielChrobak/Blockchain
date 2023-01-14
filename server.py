import hashlib
import json
import time
import os
import socket
import threading
from queue import Queue
import random
import string

class Block:
    def __init__(self, index: int, timestamp: float, transactions: list, previous_hash: str) -> None:
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        return {'block': self.index, 'timestamp': self.timestamp, 'transactions': self.transactions, 'hash': self.hash}

class Blockchain:
    def __init__(self) -> None:
        self.index = 0
        self.transaction_queue = Queue()
        if not os.path.exists("blockchain.txt"):
            self.create_genesis_block()
        else:
            last_block = self.get_previous_block()
            self.index = last_block.index + 1 if last_block else 0

    def create_new_block(self, transactions: list = None) -> Block:
        if transactions is None:
            transactions = []
        timestamp = time.time()
        previous_block = self.get_previous_block()
        previous_hash = previous_block.hash if previous_block else '0'
        new_block = Block(self.index, timestamp, transactions, previous_hash)
        self.write_to_file(new_block)
        self.index += 1
        return new_block

    def get_previous_block(self) -> Block:
        try:
            with open("blockchain.txt", "r") as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1]
                    block_data = json.loads(last_line)
                    return Block(block_data['block'], block_data['timestamp'], block_data['transactions'], block_data['hash'])
                else:
                    return None
        except FileNotFoundError:
            return None

    def write_to_file(self, new_block):
            data = {'block': new_block.index, 'timestamp': new_block.timestamp, 'transactions': new_block.transactions, 'hash': new_block.hash}
            with open("blockchain.txt", "a+") as f:
                json.dump(data, f)
                f.write('\n')
            with open("wallets.txt", "a+") as f:
                pass
            # update the balance for each address
            for transaction in new_block.transactions:
                line_ = 0
                if isinstance(transaction, str):
                    try:
                        transaction = json.loads(transaction)
                    except ValueError:
                        print("Error: transaction is not a valid json string.")
                        continue
                with open("wallets.txt", "r") as f:
                    wallets = [json.loads(l) for l in f.readlines()]
                if transaction['type'] == 'create_wallet':
                    while True:
                        wallet_id = self.generate_wallet_address()
                        if wallet_id not in wallets:
                            break
                    data = {'wallet': wallet_id, 'balance': 0}
                    with open("wallets.txt", "a+") as f:
                        json.dump(data, f)
                        f.write('\n')
                elif transaction['type'] == 'add_balance':
                    for line in wallets:
                        line_ = line_ + 1
                        if transaction['data']['wallet'] == line['wallet']:
                            print("Passed")
                    else:
                        pass
                elif transaction['type'] == 'subtract_balance':
                    if transaction['data']['address'] in self.balances:
                        self.balances[transaction['data']['address']] -= transaction['data']['amount']
                    else:
                        print("Warning: address not found in balances: ", transaction['data']['address'])
            
    def generate_wallet_address(self):
        characters = string.ascii_letters + string.digits
        address = "".join(random.choice(characters) for _ in range(20))
        hashed_address = hashlib.sha256(address.encode()).hexdigest()
        return hashed_address

    def create_genesis_block(self) -> None:
        new_block = self.create_new_block([{'type': 'genesis', 'data': 'Genesis Block'}])
        self.index = 1

    def listen_for_transactions(self):
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # Bind the socket to a specific address and port
        s.bind(('localhost', 8080))
        # Listen for incoming connections
        s.listen(1)
        print("Listening for incoming transactions...")
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # The data received is in bytes, so it needs to be decoded
                    data = json.loads(data.decode())
                    # Add the transaction to the current block
                    print("Received transaction: ", data)
                    self.transaction_queue.put(data)

    
    def create_new_block_loop(self):
        while True:
            transactions = []
            for i in range(5):
                # Wait for new transactions to arrive in the queue
                if self.transaction_queue.empty():
                    time.sleep(1)
                else:
                    transactions.extend(self.transaction_queue.get()['transactions'])
            # Create a new block with the transactions from the queue
            self.create_new_block(transactions)


if __name__ == "__main__":
    blockchain = Blockchain()
    # Create two new threads
    listen_thread = threading.Thread(target=blockchain.listen_for_transactions)
    create_thread = threading.Thread(target=blockchain.create_new_block_loop)
    # Start the threads
    listen_thread.start()
    create_thread.start()
