import hashlib
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

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


class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.chain = [self.create_genesis_block()]

    def now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        # Skip balance check for mining rewards
        if sender != "NETWORK":
            sender_balance = self.get_balance(sender)

            if sender_balance < amount:
                print(
                    f"❌ Transaction rejected: {sender} "
                    f"only has {sender_balance} NOV"
                )
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

        return True


# ------------------------------------------------
# WALLET ADDRESSES
# ------------------------------------------------

ARY = "NOV7BB05E747ACC1A1152F3613FF7FFB71478B85584"
JARVIS = "NOV8A3F1D4E7B2C5F9A1D6E3C7B4F2A8D5E1C9B3"


# ------------------------------------------------
# CREATE BLOCKCHAIN
# ------------------------------------------------

novos = Blockchain()


# ------------------------------------------------
# TRANSACTIONS
# ------------------------------------------------

# Mining reward
novos.add_transaction("NETWORK", ARY, 50)

# ARY sends 10 NOV to JARVIS
novos.add_transaction(ARY, JARVIS, 10)

# JARVIS sends 3 NOV back to ARY
novos.add_transaction(JARVIS, ARY, 3)

# Invalid transaction (JARVIS only has 7 NOV)
novos.add_transaction(JARVIS, ARY, 100)


# ------------------------------------------------
# PRINT BLOCKCHAIN
# ------------------------------------------------

print("🚀 FINAL NOVOS CHAIN\n")

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
print(f"ARY ADDRESS    : {ARY}")
print(f"ARY BALANCE    : {novos.get_balance(ARY)} NOV\n")

print(f"JARVIS ADDRESS : {JARVIS}")
print(f"JARVIS BALANCE : {novos.get_balance(JARVIS)} NOV")