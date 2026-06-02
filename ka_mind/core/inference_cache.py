"""
InferenceCache — Pre-computed paths for fast inference.
Caches query→response pairs and reasoning chains.
"""
import time
from collections import OrderedDict
from typing import Optional, List, Tuple


class InferenceCache:
    """LRU cache for inference results."""

    def __init__(self, max_size: int = 10000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self._cache: OrderedDict = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, query: str) -> Optional[str]:
        """Get cached response for a query."""
        key = query.lower().strip()[:200]
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry["time"] < self.ttl:
                self._hits += 1
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return entry["response"]
            else:
                del self._cache[key]
        self._misses += 1
        return None

    def set(self, query: str, response: str):
        """Cache a query→response pair."""
        key = query.lower().strip()[:200]
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)  # Remove oldest
        self._cache[key] = {"response": response, "time": time.time()}

    def clear(self):
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return (self._hits / total * 100) if total > 0 else 0.0

    @property
    def size(self) -> int:
        return len(self._cache)

    def stats(self) -> dict:
        return {
            "size": self.size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{self.hit_rate:.1f}%"
        }
