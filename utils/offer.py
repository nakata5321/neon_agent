from dataclasses import dataclass

@dataclass
class Offer:
    model: str
    objective: str
    token: str
    cost: str
    validator: str
    lighthouse: str
    lighthouseFee: int
    deadline: str
    sender: str
    nonce: str