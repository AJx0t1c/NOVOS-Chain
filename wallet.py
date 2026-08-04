from ecdsa import SigningKey, SECP256k1
import hashlib

# Generate private key
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

# Create address
address = hashlib.sha256(public_key.to_string()).hexdigest()[:40]

print("PRIVATE KEY:")
print(private_key.to_string().hex())

print("\nPUBLIC KEY:")
print(public_key.to_string().hex())

print("\nNOVOS ADDRESS:")
print("NOV" + address.upper())