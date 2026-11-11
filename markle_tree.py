import hashlib


def hash_leaf(data: str) -> bytes:
    return hashlib.sha256(b"\x00" + data.encode("utf-8")).digest()

def hash_pair(a: bytes, b: bytes) -> bytes:
    if a>b:
        a,b = b,a
    return hashlib.sha256(b"\x01" + a + b).digest()

def build_tree_and_proof(items: list[str], target_index: str):
    level = [hash_leaf(item) for item in items]
    proof = []
    idx = target_index

    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            if i+1<len(level):
                if idx == i:
                    proof.append(level[i+1])
                elif idx == i+1:
                    proof.append(level[i])
                next_level.append(hash_pair(level[i], level[i+1]))

            else:
                next_level.append(level[i])

        idx //= 2
        level = next_level

    return level[0], proof


def verify_proof(root: bytes, item: str, proof: list[bytes]) -> bool:
    current = hash_leaf(item)
    for sibling in proof:
        current = hash_pair(current, sibling)
    return current == root


users = ["Аня", "Боря", "Ваня", "Глеб", "Дима"]
root, proof_for_vanya = build_tree_and_proof(users, target_index=2)

print("Markle root: ", root.hex())
print("Длина proof: ", len(proof_for_vanya), "хеша(ей)")
print("Ваня в списке? ", verify_proof(root, "Ваня", proof_for_vanya))
print("Даня в списке? ", verify_proof(root, "Даня", proof_for_vanya))