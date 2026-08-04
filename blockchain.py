import hashlib
import json
import os
from datetime import datetime
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError


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

    # ------------------------------------------------
    # VERIFY DIGITAL SIGNATURE
    # ------------------------------------------------

    def verify_transaction(self, transaction):
        try:
            public_key = VerifyingKey.from_string(
                bytes.fromhex(transaction["public_key"]),
                curve=SECP256k1
            )

            message = json.dumps({
                "from": transaction["from"],
                "to": transaction["to"],
                "amount": transaction["amount"]
            }, sort_keys=True).encode()

            public_key.verify(
                bytes.fromhex(transaction["signature"]),
                message
            )

            return True

        except BadSignatureError:
            return False
        except Exception:
            return False

    # ------------------------------------------------
    # ADD TRANSACTION
    # ------------------------------------------------

    def add_transaction(self, transaction):
        sender = transaction["from"]
        receiver = transaction["to"]
        amount = transaction["amount"]

        # Skip signature check for mining rewards
        if sender != "NETWORK":
            if not self.verify_transaction(transaction):
                print("❌ Invalid digital signature")
                return False

            sender_balance = self.get_balance(sender)

            if sender_balance < amount:
                print(f"❌ Transaction rejected: {sender} only has {sender_balance} NOV")
                return False

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

ARY = "NOV7EFE051755AB888BFF407609F3E5583EBF75A982"
JARVIS = "NOV9E9BC65D129F5EEF80C4E302AE928B3E72B9B1E7"


# ------------------------------------------------
# CREATE / LOAD BLOCKCHAIN
# ------------------------------------------------

novos = Blockchain()


# ------------------------------------------------
# EXAMPLE SIGNED TRANSACTION
# ------------------------------------------------

# NETWORK rewards don't need signatures
if len(novos.chain) == 1:
    novos.add_transaction({
        "from": "NETWORK",
        "to": ARY,
        "amount": 50
    })

    print("\n⚠️ To create real signed transactions, use wallet.py\n")


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