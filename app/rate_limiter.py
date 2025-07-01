import time
from collections import defaultdict

_WINDOW = 60  # seconds

class MemoryRateLimiter:
    def __init__(self, limit: int):
        self.limit = limit
        self.hits: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - _WINDOW
        self.hits[key] = [t for t in self.hits[key] if t >= window_start]
        if len(self.hits[key]) >= self.limit:
            return False
        self.hits[key].append(now)
        return True