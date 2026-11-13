import secrets
from eth_account import Account
from eth_account.messages import encode_defunct
from nacl.signing import SigningKey
import base58

priv_bytes = secrets.token_bytes(32)
eth_acc = Account.from_key(priv_bytes)


print("PRIVATE KEY: ", priv_bytes.hex())
print("The sender address: ", eth_acc.address)


tx = {
    "nonce": 0,
    "to": "0x000000000000000000000000000000000000dEaD",
    "value": 1_000_000_000_000_000_000,
    "gas": 21000,
    "gasPrice": 20_000_000_000,
    "chainId": 1
}

signed_tx = eth_acc.sign_transaction(tx)

v = signed_tx.v
r = signed_tx.r
s = signed_tx.s


print("Компоненты подписи (v, s, r)")
print(f"v(recovery id): {v}")
print(f"r: {hex(r)}")
print(f"s: {hex(s)}")


recovered_address_a = Account.recover_transaction(signed_tx.raw_transaction)

r_bytes = r.to_bytes(32, byteorder="big")
s_bytes = s.to_bytes(32, byteorder="big")

recovery_id = v - (tx["chainId"] * 2 + 35)
v_standart = 27+recovery_id
signature_bytes = r_bytes + s_bytes + bytes([v_standart])

recovered_address_b = Account._recover_hash(signed_tx.hash, signature=signature_bytes)

print("Проверка восстановления")
print("Восстановленный адрес(A): ", recovered_address_a)
print("Восстановленный адрес(B): ", recovered_address_b)
print("Совпадает с оригиналом A? ", recovered_address_a == eth_acc.address)
print("Совпадает с оригиналом B? ", recovered_address_b == eth_acc.address)


#solana

signing_key = SigningKey(priv_bytes)
verify_key = signing_key.verify_key

sol_key = SigningKey(priv_bytes)
sol_address = base58.b58encode(bytes(sol_key.verify_key)).decode()

full_private_key = bytes(signing_key) + bytes(verify_key)
sol_private_key_b58 = base58.b58encode(full_private_key).decode()

print("SOLANA")
print("Public SOL Address: ", sol_address)
print("Private key(Base58): ", sol_private_key_b58)
