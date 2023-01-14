import json
from datetime import datetime

def read_blockchain():
    with open("blockchain.txt", "r") as f:
        for line in f:
            block = json.loads(line)
            timestamp = block['timestamp']
            readable_timestamp = convert_timestamp(timestamp)
            print(f"Block: {block['block']}")
            print(f"Timestamp: {readable_timestamp}")
            print(f"Data: {block['transactions'][0]['data']}")
            print(f"Hash: {block['hash']}")
            print()

def convert_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

read_blockchain()
