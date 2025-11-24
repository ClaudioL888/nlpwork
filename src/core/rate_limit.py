from __future__ import annotations

import time
from collections import defaultdict, deque


class InMemoryRateLimiter:
    def __init__(self, max_events: int, per_seconds: int) -> None:
        self.max_events = max_events
        self.per_seconds = per_seconds
        self.events: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> bool:
        window_start = time.time() - self.per_seconds
        dq = self.events[key]
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= self.max_events:
            return False
        dq.append(time.time())
        return True
