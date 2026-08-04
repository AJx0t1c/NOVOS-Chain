import hashlib
import json
import os
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, hash_value=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash_value or self.calculate_hash()

    def calculate_hash(self):
        text = (
            f"{self.index}{self.timestamp}"
            f"{self.data}{self.previous_hash}{self.nonce}"
        )
        return hashlib.sha256(text.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"⛏️ Block {self.index} mined!")
        print(f"Nonce: {self.nonce}")
        print(f"Hash : {self.hash}\n")

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.chain = []

        self.load_chain()

        if not self.chain:
            genesis = self.create_genesis_block()
            self.chain.append(genesis)
            self.save_chain()

    def now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def create_genesis_block(self):
        block = Block(
            0,
            self.now(),
            "Genesis Block - NOVOS Chain",
            "0"
        )
        block.mine(self.difficulty)
        return block

    def get_latest_block(self):
        return self.chain[-1]

    def save_chain(self):
        with open("chain.json", "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        if os.path.exists("chain.json"):
            with open("chain.json", "r") as f:
                data = json.load(f)

            self.chain = [
                Block(
                    block["index"],
                    block["timestamp"],
                    block["data"],
                    block["previous_hash"],
                    block["nonce"],
                    block["hash"]
                )
                for block in data
            ]

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            data = block.data

            if isinstance(data, dict):
                if data.get("from") == address:
                    balance -= data.get("amount", 0)

                if data.get("to") == address:
                    balance += data.get("amount", 0)

        return balance

    def add_transaction(self, sender, receiver, amount):
        if sender != "NETWORK":
            sender_balance = self.get_balance(sender)

            if sender_balance < amount:
                print(f"❌ Transaction rejected: {sender} only has {sender_balance} NOV")
                return False

        transaction = {
            "from": sender,
            "to": receiver,
            "amount": amount
        }

        latest = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            self.now(),
            transaction,
            latest.hash
        )

        new_block.mine(self.difficulty)
        self.chain.append(new_block)

        self.save_chain()

        return True


# ------------------------------------------------
# WALLET ADDRESSES
# ------------------------------------------------

ARY = "NOV7BB05E747ACC1A1152F3613FF7FFB71478B85584"
JARVIS = "NOV8A3F1D4E7B2C5F9A1D6E3C7B4F2A8D5E1C9B3"


# ------------------------------------------------
# CREATE / LOAD BLOCKCHAIN
# ------------------------------------------------

novos = Blockchain()


# ------------------------------------------------
# ADD NEW TRANSACTIONS
# ------------------------------------------------

# These will only be added the first time you run the file
if len(novos.chain) == 1:
    novos.add_transaction("NETWORK", ARY, 50)
    novos.add_transaction(ARY, JARVIS, 10)
    novos.add_transaction(JARVIS, ARY, 3)


# ------------------------------------------------
# PRINT BLOCKCHAIN
# ------------------------------------------------

print("🚀 NOVOS CHAIN\n")

for block in novos.chain:
    print("====================")
    print(f"Block #{block.index}")
    print(f"Timestamp     : {block.timestamp}")
    print(f"Data          : {block.data}")
    print(f"Nonce         : {block.nonce}")
    print(f"Previous Hash : {block.previous_hash}")
    print(f"Hash          : {block.hash}\n")


# ------------------------------------------------
# PRINT BALANCES
# ------------------------------------------------

print("💰 WALLET BALANCES\n")
print(f"ARY BALANCE    : {novos.get_balance(ARY)} NOV")
print(f"JARVIS BALANCE : {novos.get_balance(JARVIS)} NOV")