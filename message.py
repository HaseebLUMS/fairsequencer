class Message:
    def __init__(self, ts): self.ts = ts
    def get_ts(self) -> int: 
        return self.ts
    def __repr__(self) -> str:
        return f"Message(ts={self.ts})"