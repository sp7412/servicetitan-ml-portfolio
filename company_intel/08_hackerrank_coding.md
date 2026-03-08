# 08 — HackerRank Coding Patterns & Solutions

Based on reported ServiceTitan interview experience (Glassdoor, Feb 2026):
> "They ask you to implement a custom data structure to a given interface."
> "Part 1 straightforward, Part 2 more complex. Example: MultiMap."

---

## Pattern: Implement a Custom Data Structure

### Example Problem: MultiMap

A MultiMap maps keys to *lists* of values (unlike a regular map which maps to a single value).

**Interface:**
```python
class MultiMap:
    def put(self, key, value) -> None
    def get(self, key) -> list          # returns all values for key, or []
    def remove(self, key, value) -> bool # removes one instance of value from key
    def keys(self) -> list              # all keys with at least one value
    def size(self) -> int               # total number of (key, value) pairs
```

**Part 1 — Basic Implementation:**

```python
from collections import defaultdict

class MultiMap:
    def __init__(self):
        self._data = defaultdict(list)  # O(1) average access
    
    def put(self, key, value) -> None:
        # O(1) amortized -- list.append is amortized O(1)
        self._data[key].append(value)
    
    def get(self, key) -> list:
        # O(1) -- returns reference to existing list
        # Return a copy so callers can't mutate internal state
        return list(self._data[key])
    
    def remove(self, key, value) -> bool:
        # O(n) where n = number of values for this key
        # Scans list to find first occurrence of value
        if key in self._data and value in self._data[key]:
            self._data[key].remove(value)   # removes first occurrence
            if not self._data[key]:         # clean up empty keys
                del self._data[key]
            return True
        return False
    
    def keys(self) -> list:
        # O(k) where k = number of distinct keys
        return list(self._data.keys())
    
    def size(self) -> int:
        # O(k) -- sum over all key lists
        return sum(len(v) for v in self._data.values())
```

**Complexity Summary (Part 1):**

| Operation | Time | Space |
|---|---|---|
| `put(k, v)` | O(1) amortized | O(1) |
| `get(k)` | O(n) for copy | O(n) |
| `remove(k, v)` | O(n) scan | O(1) |
| `keys()` | O(k) | O(k) |
| `size()` | O(k) | O(1) |
| Space overall | — | O(N) where N = total pairs |

**Part 2 — Advanced Features:**

*Common Part 2 asks: O(1) `size()`, ordered keys, `get_all_values()`, thread safety*

```python
from collections import defaultdict
import threading

class MultiMapV2:
    """
    Optimized MultiMap with O(1) size(), sorted keys, and thread safety.
    Tradeoff: O(log k) put/remove for sorted key maintenance vs O(1) basic.
    """
    def __init__(self):
        self._data  = defaultdict(list)
        self._size  = 0                    # cached total -- O(1) size()
        self._lock  = threading.RLock()    # reentrant for nested calls
    
    def put(self, key, value) -> None:
        with self._lock:
            self._data[key].append(value)
            self._size += 1
    
    def get(self, key) -> list:
        with self._lock:
            return list(self._data.get(key, []))
    
    def remove(self, key, value) -> bool:
        with self._lock:
            vals = self._data.get(key)
            if vals and value in vals:
                vals.remove(value)
                self._size -= 1
                if not vals:
                    del self._data[key]
                return True
            return False
    
    def remove_all(self, key) -> int:
        """Remove all values for a key. Returns count removed."""
        with self._lock:
            if key in self._data:
                count = len(self._data[key])
                del self._data[key]
                self._size -= count
                return count
            return 0
    
    def keys(self) -> list:
        with self._lock:
            return sorted(self._data.keys())    # O(k log k)
    
    def size(self) -> int:
        return self._size                       # O(1) -- cached
    
    def get_all_values(self) -> list:
        """Returns flat list of all values across all keys."""
        with self._lock:
            return [v for vals in self._data.values() for v in vals]
    
    def invert(self) -> 'MultiMapV2':
        """Returns a new MultiMap with keys and values swapped."""
        with self._lock:
            inv = MultiMapV2()
            for k, vals in self._data.items():
                for v in vals:
                    inv.put(v, k)
            return inv
```

**Tradeoffs: Part 2 Design Decisions**

| Feature | Choice | Tradeoff |
|---|---|---|
| O(1) size() | Cache `_size` counter | Extra state to keep consistent; bugs if you forget to update |
| Sorted keys() | `sorted()` on call | O(k log k) on every keys() call vs O(k log k) on every insert with SortedList |
| Thread safety | `threading.RLock` | Serializes all operations; hurts throughput; use per-key locks for higher perf |
| Copy-on-get | `list(...)` copy | Prevents external mutation; O(n) cost vs O(1) view |
| Clean empty keys | `del self._data[key]` | Prevents memory leak; extra branch per remove |

---

## Pattern: Async/Await + Parallel Programming

*Reported in Part 2 of ServiceTitan HackerRank*

```python
import asyncio
import aiohttp
from typing import List

# Pattern: fetch multiple URLs concurrently
async def fetch_one(session, url: str) -> dict:
    async with session.get(url) as response:
        return {"url": url, "status": response.status, "body": await response.text()}

async def fetch_all(urls: List[str]) -> List[dict]:
    """
    O(max_single_latency) instead of O(sum_all_latencies)
    asyncio.gather fires all requests concurrently, awaits all to complete.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

# Bounded concurrency (semaphore) -- avoid hammering the server
async def fetch_all_bounded(urls: List[str], max_concurrent: int = 10) -> List[dict]:
    sem = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_limit(session, url):
        async with sem:                         # only max_concurrent at a time
            return await fetch_one(session, url)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

**Complexity:**
- Serial fetches: O(n * avg_latency)
- `asyncio.gather`: O(max_single_latency) -- all run in parallel
- With semaphore(k): O(ceil(n/k) * avg_latency)

---

## Pattern: LRU Cache

*Classic "implement a data structure" — appears frequently*

```python
from collections import OrderedDict

class LRUCache:
    """
    O(1) get and put using OrderedDict (doubly linked list + hash map).
    OrderedDict.move_to_end() is O(1); popitem(last=False) removes oldest.
    """
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()  # maintains insertion order
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)      # mark as recently used
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)   # evict least recently used
    
    # O(1) get, O(1) put, O(capacity) space
```

---

## Pattern: Priority Queue (Heap)

*Common in dispatch/scheduling problems*

```python
import heapq

class JobScheduler:
    """
    Min-heap by priority. O(log n) push/pop, O(1) peek.
    Common pattern: (priority, tie_breaker, item) tuple for stable sort.
    """
    def __init__(self):
        self._heap = []
        self._counter = 0  # tie-breaker: insertion order
    
    def push(self, job_id: str, priority: float):
        # Negate priority for max-heap behavior (highest value = first out)
        heapq.heappush(self._heap, (-priority, self._counter, job_id))
        self._counter += 1
    
    def pop(self) -> str:
        # O(log n)
        if not self._heap:
            raise IndexError("empty scheduler")
        _, _, job_id = heapq.heappop(self._heap)
        return job_id
    
    def peek(self) -> str:
        # O(1)
        return self._heap[0][2] if self._heap else None
    
    def __len__(self): return len(self._heap)
```

---

## Interview Tips

1. **State your interface first** — read the problem, write out the method signatures with types before coding
2. **Declare complexity up front** — "I'll aim for O(1) put and O(log n) get" before you start
3. **Comment the tradeoffs** — they want to see you understand why you made each choice
4. **Test with edge cases** — empty map, duplicate keys, removing non-existent value, capacity-0 LRU
5. **Ask about thread safety** — even if they don't ask, mention it: "If this were concurrent I'd add a lock here"
6. **Don't over-engineer Part 1** — simple and correct beats complex and buggy; save cleverness for Part 2
7. **`defaultdict` is your friend** — eliminates key-existence checks in map problems
