from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib
import json


class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    @property
    def address(self):
        return "NOV" + hashlib.sha256(
            self.public_key.to_string()
        ).hexdigest()[:40].upper()

    def sign_transaction(self, sender, receiver, amount):
        transaction = {
            "from": sender,
            "to": receiver,
            "amount": amount
        }

        message = json.dumps(transaction, sort_keys=True).encode()
        signature = self.private_key.sign(message).hex()

        transaction["public_key"] = self.public_key.to_string().hex()
        transaction["signature"] = signature

        return transaction


if __name__ == "__main__":
    wallet = Wallet()

    print("ADDRESS:")
    print(wallet.address)

    print("\nPRIVATE KEY:")
    print(wallet.private_key.to_string().hex())