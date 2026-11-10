from dataclasses import dataclass, field
import hashlib, json, time
import json


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: list[dict]
    prev_hash: str
    nonce: int = 0
    hash: str = field(init=False)

    def __post_init__(self):
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
        }, sort_keys=True).encode("utf-8")

        return hashlib.sha256(payload).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """The first block in chain"""
        genesis = Block(
            index=0,
            timestamp=0.0,
            transactions=[{"info": "Genesis block"}],
            prev_hash="0" * 64,
        )
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, transactions: list[dict]) -> Block:
        """Creates the new block, connects it to the prev hash"""
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            prev_hash=self.last_block.hash,
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Checks the integrity of all chain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]

            if current.hash != current.compute_hash():
                print(f"[ERROR] The block #{current.index} was modified!")
                return False

            if current.prev_hash != prev.hash:
                print(f"[ERROR] The connection between #{prev.index} and #{current.index} was broken!")
                return False

        return True

if __name__ == "__main__":
    bc = Blockchain()

    bc.add_block([{"from": "Alice", "to": "Bob", "amount": 10}])
    bc.add_block([{"from": "Bob", "to": "Charlie", "amount": 4}])

    print("1. Checking the correctness of the chain: ")
    print("Is the chain valid? ", bc.is_chain_valid())

    print("2. Modelling the attack(changing the sum in the block 1): ")
    bc.chain[1].transactions[0]["amount"] = 99999

    print("Is the chain valid after attack?")
    print("Result: ", bc.is_chain_valid())