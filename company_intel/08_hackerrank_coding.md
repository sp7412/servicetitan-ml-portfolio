# 08 — HackerRank Coding Patterns & Solutions

## Overview: What to Expect

**Format:** 90-minute online coding assessment on HackerRank platform
**Structure:** Usually 2 problems
- **Part 1:** Straightforward implementation (30-40 minutes)
- **Part 2:** More complex variant or optimization (40-50 minutes)

**Common Themes Based on Glassdoor Reports:**
- "Implement a custom data structure to a given interface"
- "MultiMap was the example given"
- "Part 1 was basic, Part 2 added concurrency/optimization requirements"
- "Focus on clean code, edge cases, and explaining tradeoffs"

**What ServiceTitan Looks For:**
1. **Correctness** - Does it work for all test cases?
2. **Code quality** - Clean, readable, well-structured
3. **Complexity analysis** - Can you explain time/space tradeoffs?
4. **Edge case handling** - Empty inputs, duplicates, boundary conditions
5. **Communication** - Comments explaining design decisions

---

## Background: Why These Patterns?

ServiceTitan's platform deals with:
- **High-volume data:** Millions of jobs, calls, technicians
- **Real-time systems:** Dispatch, call routing, notifications
- **Caching:** Performance optimization for multi-tenant SaaS
- **Concurrency:** Multiple users accessing same data

These coding patterns test your ability to build the data structures that power these systems.

---

## Pattern 1: Custom Data Structure (MultiMap)

### Why This Matters at ServiceTitan

**Real-world use case:** A technician can have multiple skills, a job can have multiple parts, a customer can have multiple properties.

```python
# Example: Technician skills mapping
skills_map = MultiMap()
skills_map.put("tech_001", "HVAC")
skills_map.put("tech_001", "Plumbing")
skills_map.put("tech_001", "Electrical")

# When dispatching a job requiring HVAC, find all qualified techs
hvac_techs = skills_map.get("HVAC")  # Returns list of tech IDs
```

### Problem Statement (Typical)

**Part 1: Basic MultiMap**

Implement a `MultiMap` class that maps keys to **lists** of values (unlike a regular dictionary which maps to a single value).

**Interface:**
```python
class MultiMap:
    def put(self, key, value) -> None:
        """Add a value to the list for this key."""
        pass
    
    def get(self, key) -> list:
        """Return all values for this key, or empty list if key doesn't exist."""
        pass
    
    def remove(self, key, value) -> bool:
        """Remove one instance of value from key's list. Return True if found."""
        pass
    
    def keys(self) -> list:
        """Return all keys that have at least one value."""
        pass
    
    def size(self) -> int:
        """Return total number of (key, value) pairs."""
        pass
```

**Example Usage:**
```python
mm = MultiMap()
mm.put("colors", "red")
mm.put("colors", "blue")
mm.put("colors", "red")      # duplicates allowed
mm.get("colors")              # ["red", "blue", "red"]
mm.remove("colors", "red")    # True (removes first occurrence)
mm.get("colors")              # ["blue", "red"]
mm.size()                     # 2
mm.keys()                     # ["colors"]
```

### Solution: Part 1 (Basic Implementation)

```python
from collections import defaultdict
from typing import Any, List

class MultiMap:
    """
    A map that associates keys with lists of values.
    
    Design decisions:
    - Use defaultdict(list) for automatic list initialization
    - Return copies of internal lists to prevent external mutation
    - Clean up empty keys to avoid memory leaks
    - All operations are straightforward with acceptable complexity
    """
    
    def __init__(self):
        # defaultdict automatically creates empty list for new keys
        # This eliminates need for "if key not in dict" checks
        self._data = defaultdict(list)
    
    def put(self, key: Any, value: Any) -> None:
        """
        Add a value to the list for this key.
        
        Time: O(1) amortized - list.append is amortized O(1)
        Space: O(1) for this operation
        """
        self._data[key].append(value)
    
    def get(self, key: Any) -> List[Any]:
        """
        Return all values for this key.
        
        Time: O(n) where n = number of values for this key (for copying)
        Space: O(n) for the copy
        
        Why copy? Prevents caller from mutating internal state:
        >>> mm.get("key").append("bad")  # Won't affect internal data
        """
        return list(self._data[key])  # Returns copy, not reference
    
    def remove(self, key: Any, value: Any) -> bool:
        """
        Remove first occurrence of value from key's list.
        
        Time: O(n) where n = number of values for this key
              (list.remove scans to find first match)
        Space: O(1)
        
        Edge cases handled:
        - Key doesn't exist: return False
        - Value not in list: return False
        - After removal, list is empty: delete key to avoid memory leak
        """
        if key in self._data and value in self._data[key]:
            self._data[key].remove(value)  # Removes first occurrence only
            
            # Clean up: remove key if no values left
            # This prevents memory leak from empty lists
            if not self._data[key]:
                del self._data[key]
            
            return True
        return False
    
    def keys(self) -> List[Any]:
        """
        Return all keys that have at least one value.
        
        Time: O(k) where k = number of distinct keys
        Space: O(k) for the list
        """
        return list(self._data.keys())
    
    def size(self) -> int:
        """
        Return total number of (key, value) pairs.
        
        Time: O(k) where k = number of distinct keys
              (must sum lengths of all lists)
        Space: O(1)
        
        Note: This is O(k), not O(1). Part 2 often asks for O(1) size().
        """
        return sum(len(values) for values in self._data.values())


# ============================================================================
# TEST CASES - Always include these in your submission
# ============================================================================

def test_multimap_basic():
    """Test basic functionality."""
    mm = MultiMap()
    
    # Test empty map
    assert mm.size() == 0
    assert mm.keys() == []
    assert mm.get("nonexistent") == []
    
    # Test put and get
    mm.put("colors", "red")
    mm.put("colors", "blue")
    assert mm.size() == 2
    assert set(mm.get("colors")) == {"red", "blue"}
    
    # Test duplicates
    mm.put("colors", "red")
    assert mm.size() == 3
    assert mm.get("colors").count("red") == 2
    
    # Test remove
    assert mm.remove("colors", "red") == True
    assert mm.size() == 2
    assert mm.get("colors").count("red") == 1
    
    # Test remove nonexistent
    assert mm.remove("colors", "green") == False
    assert mm.remove("invalid_key", "value") == False
    
    # Test key cleanup after removing all values
    mm.remove("colors", "red")
    mm.remove("colors", "blue")
    assert "colors" not in mm.keys()
    assert mm.size() == 0
    
    print("✓ All basic tests passed")


def test_multimap_edge_cases():
    """Test edge cases."""
    mm = MultiMap()
    
    # None as key/value
    mm.put(None, "value")
    mm.put("key", None)
    assert mm.get(None) == ["value"]
    assert mm.get("key") == [None]
    
    # Empty string
    mm.put("", "empty_key")
    assert mm.get("") == ["empty_key"]
    
    # Large number of values
    for i in range(1000):
        mm.put("large", i)
    assert mm.size() == 1002  # 1000 + 2 from above
    
    print("✓ All edge case tests passed")


if __name__ == "__main__":
    test_multimap_basic()
    test_multimap_edge_cases()
```

**Complexity Summary (Part 1):**

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `put(k, v)` | O(1) amortized | O(1) | List append is amortized O(1) |
| `get(k)` | O(n) | O(n) | n = values for key; O(n) for copy |
| `remove(k, v)` | O(n) | O(1) | n = values for key; linear scan |
| `keys()` | O(k) | O(k) | k = number of distinct keys |
| `size()` | O(k) | O(1) | Must sum all list lengths |
| **Overall space** | — | O(N) | N = total (key, value) pairs |

---

### Part 2: Advanced Features

**Common Part 2 Requirements:**
1. **O(1) size()** - Cache the total count
2. **Thread safety** - Multiple threads accessing simultaneously
3. **Ordered keys** - Return keys in sorted order
4. **Additional methods** - `remove_all()`, `get_all_values()`, `invert()`
5. **Memory optimization** - Handle millions of entries efficiently

**Why These Matter:**
- **O(1) size()**: ServiceTitan dashboards show counts in real-time
- **Thread safety**: Multiple API requests accessing same data
- **Ordered keys**: Consistent UI display, easier debugging
- **Bulk operations**: Batch processing for efficiency

### Solution: Part 2 (Optimized Implementation)

```python
from collections import defaultdict
from typing import Any, List, Dict
import threading

class MultiMapV2:
    """
    Optimized MultiMap with O(1) size(), thread safety, and additional features.
    
    Key optimizations:
    1. Cached _size counter for O(1) size() queries
    2. threading.RLock for thread-safe operations
    3. Additional bulk operations for efficiency
    4. Sorted keys() for consistent ordering
    
    Tradeoffs:
    - More complex code (more state to maintain)
    - Lock contention can hurt throughput under high concurrency
    - sorted() on keys() is O(k log k) vs O(k) unsorted
    """
    
    def __init__(self):
        self._data = defaultdict(list)
        self._size = 0  # Cached total count - MUST keep in sync!
        
        # RLock (reentrant lock) allows same thread to acquire multiple times
        # Needed if one method calls another (e.g., remove_all calls remove)
        self._lock = threading.RLock()
    
    def put(self, key: Any, value: Any) -> None:
        """
        Thread-safe put with O(1) size update.
        
        Time: O(1) amortized
        Space: O(1)
        """
        with self._lock:  # Acquire lock for entire operation
            self._data[key].append(value)
            self._size += 1  # Keep counter in sync
    
    def get(self, key: Any) -> List[Any]:
        """
        Thread-safe get.
        
        Time: O(n) where n = values for key
        Space: O(n)
        
        Note: We copy the list while holding the lock to ensure
        consistency (no concurrent modifications during copy).
        """
        with self._lock:
            return list(self._data.get(key, []))
    
    def remove(self, key: Any, value: Any) -> bool:
        """
        Thread-safe remove with O(1) size update.
        
        Time: O(n) where n = values for key
        Space: O(1)
        """
        with self._lock:
            vals = self._data.get(key)
            if vals and value in vals:
                vals.remove(value)
                self._size -= 1  # Keep counter in sync
                
                # Clean up empty keys
                if not vals:
                    del self._data[key]
                
                return True
            return False
    
    def remove_all(self, key: Any) -> int:
        """
        Remove all values for a key. Returns count of values removed.
        
        Time: O(1) - just delete the key
        Space: O(1)
        
        This is more efficient than calling remove() repeatedly.
        """
        with self._lock:
            if key in self._data:
                count = len(self._data[key])
                del self._data[key]
                self._size -= count  # Keep counter in sync
                return count
            return 0
    
    def keys(self) -> List[Any]:
        """
        Return all keys in sorted order.
        
        Time: O(k log k) where k = number of keys
        Space: O(k)
        
        Tradeoff: sorted() adds O(k log k) cost but gives consistent ordering.
        Alternative: maintain a SortedList and update on every put/remove
        for O(log k) per operation but O(k) keys() call.
        """
        with self._lock:
            return sorted(self._data.keys())
    
    def size(self) -> int:
        """
        Return total number of (key, value) pairs.
        
        Time: O(1) - cached counter
        Space: O(1)
        
        This is the key optimization for Part 2!
        """
        return self._size  # No lock needed - atomic read
    
    def get_all_values(self) -> List[Any]:
        """
        Return flat list of all values across all keys.
        
        Time: O(N) where N = total values
        Space: O(N)
        
        Use case: "Show me all skills across all technicians"
        """
        with self._lock:
            return [v for vals in self._data.values() for v in vals]
    
    def invert(self) -> 'MultiMapV2':
        """
        Return a new MultiMap with keys and values swapped.
        
        Time: O(N) where N = total (key, value) pairs
        Space: O(N) for new map
        
        Use case: "I have tech->skills, give me skill->techs"
        
        Example:
        >>> mm = MultiMapV2()
        >>> mm.put("tech1", "HVAC")
        >>> mm.put("tech1", "Plumbing")
        >>> mm.put("tech2", "HVAC")
        >>> inv = mm.invert()
        >>> inv.get("HVAC")  # ["tech1", "tech2"]
        """
        with self._lock:
            inverted = MultiMapV2()
            for key, values in self._data.items():
                for value in values:
                    inverted.put(value, key)
            return inverted
    
    def __len__(self) -> int:
        """Support len(mm) syntax."""
        return self.size()
    
    def __repr__(self) -> str:
        """Readable string representation for debugging."""
        with self._lock:
            items = {k: list(v) for k, v in self._data.items()}
            return f"MultiMapV2({items})"


# ============================================================================
# ADVANCED TEST CASES
# ============================================================================

def test_multimap_v2_thread_safety():
    """Test thread safety with concurrent operations."""
    import concurrent.futures
    
    mm = MultiMapV2()
    
    def worker(thread_id: int):
        """Each thread adds 100 values."""
        for i in range(100):
            mm.put(f"key_{thread_id % 10}", f"value_{thread_id}_{i}")
    
    # Run 10 threads concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        concurrent.futures.wait(futures)
    
    # Verify: 10 threads × 100 values = 1000 total
    assert mm.size() == 1000
    print(f"✓ Thread safety test passed: {mm.size()} values")


def test_multimap_v2_performance():
    """Test O(1) size() performance."""
    import time
    
    mm = MultiMapV2()
    
    # Add 100K values
    for i in range(100_000):
        mm.put(f"key_{i % 1000}", i)
    
    # size() should be instant (O(1))
    start = time.time()
    for _ in range(10_000):
        _ = mm.size()
    elapsed = time.time() - start
    
    assert elapsed < 0.1  # 10K calls in < 100ms
    print(f"✓ Performance test passed: 10K size() calls in {elapsed:.3f}s")


def test_multimap_v2_advanced_features():
    """Test additional methods."""
    mm = MultiMapV2()
    
    # Setup
    mm.put("tech1", "HVAC")
    mm.put("tech1", "Plumbing")
    mm.put("tech2", "HVAC")
    mm.put("tech2", "Electrical")
    
    # Test remove_all
    removed = mm.remove_all("tech1")
    assert removed == 2
    assert mm.size() == 2
    
    # Test get_all_values
    all_vals = mm.get_all_values()
    assert set(all_vals) == {"HVAC", "Electrical"}
    
    # Test invert
    mm2 = MultiMapV2()
    mm2.put("tech1", "HVAC")
    mm2.put("tech2", "HVAC")
    mm2.put("tech2", "Plumbing")
    
    inv = mm2.invert()
    assert set(inv.get("HVAC")) == {"tech1", "tech2"}
    assert inv.get("Plumbing") == ["tech2"]
    
    print("✓ Advanced features test passed")


if __name__ == "__main__":
    test_multimap_v2_thread_safety()
    test_multimap_v2_performance()
    test_multimap_v2_advanced_features()
```

**Design Tradeoffs Discussion (Critical for Interview):**

| Feature | Implementation Choice | Tradeoff | Alternative |
|---------|----------------------|----------|-------------|
| **O(1) size()** | Cache `_size` counter | Must keep in sync (bug risk) | Recompute each time: O(k) but simpler |
| **Thread safety** | Single `RLock` for all ops | Serializes everything (low throughput) | Per-key locks: higher throughput, more complex |
| **Sorted keys()** | `sorted()` on every call | O(k log k) per call | Maintain `SortedList`: O(log k) per put/remove |
| **Copy on get()** | `list(...)` copy | O(n) time + space | Return view: O(1) but caller can mutate |
| **Clean empty keys** | `del` after last remove | Prevents memory leak | Keep empty lists: simpler but wastes memory |

**Interview Tip:** Always mention these tradeoffs! Say something like:
> "I'm caching the size for O(1) queries, but this adds complexity because I need to keep it in sync. An alternative would be to recompute on every call, which is simpler but O(k). Given that size() is likely called frequently in dashboards, I think the O(1) optimization is worth it."

---

## Pattern 2: Async/Await + Parallel Programming

### Why This Matters at ServiceTitan

**Real-world use case:** Atlas AI needs to fetch data from multiple sources concurrently:
- Customer history from SQL
- Recent calls from call recording service
- Technician availability from scheduling service
- Weather data from external API

Doing these serially would take 4× as long. Async/await lets you parallelize I/O-bound operations.

### Background: Async vs Threading vs Multiprocessing

```python
# WRONG: Serial execution (slow)
def fetch_all_serial(urls):
    results = []
    for url in urls:
        results.append(requests.get(url))  # Blocks for each request
    return results
# Time: sum of all request times (e.g., 10 URLs × 200ms = 2 seconds)

# BETTER: Threading (parallel I/O)
from concurrent.futures import ThreadPoolExecutor
def fetch_all_threaded(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(requests.get, urls))
    return results
# Time: max of all request times (e.g., max(200ms) = 200ms)

# BEST: Async/await (efficient parallel I/O)
import asyncio
import aiohttp

async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results
# Time: max of all request times, but lower overhead than threading
```

**When to use each:**
- **Serial:** Never for I/O-bound tasks
- **Threading:** Good for I/O-bound, but has overhead (GIL in Python)
- **Async/await:** Best for I/O-bound, lowest overhead
- **Multiprocessing:** Only for CPU-bound tasks (not covered here)

### Problem: Fetch Multiple URLs Concurrently

```python
import asyncio
import aiohttp
from typing import List, Dict
import time

async def fetch_one(session: aiohttp.ClientSession, url: str) -> Dict:
    """
    Fetch a single URL and return result.
    
    Time: O(latency) - depends on network/server
    Space: O(response_size)
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            return {
                "url": url,
                "status": response.status,
                "body": await response.text(),
                "success": True
            }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "body": None,
            "success": False,
            "error": str(e)
        }


async def fetch_all(urls: List[str]) -> List[Dict]:
    """
    Fetch multiple URLs concurrently.
    
    Time: O(max_single_latency) instead of O(sum_all_latencies)
    Space: O(n * avg_response_size)
    
    asyncio.gather() fires all requests concurrently and waits for all to complete.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions (gather with return_exceptions=True returns them)
        return [r for r in results if not isinstance(r, Exception)]


async def fetch_all_bounded(urls: List[str], max_concurrent: int = 10) -> List[Dict]:
    """
    Fetch URLs with bounded concurrency (don't hammer the server).
    
    Time: O(ceil(n / max_concurrent) * avg_latency)
    Space: O(max_concurrent * avg_response_size)
    
    Semaphore limits how many requests run simultaneously.
    This is important to avoid:
    - Overwhelming the target server
    - Running out of file descriptors
    - Excessive memory usage
    """
    sem = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_limit(session, url):
        async with sem:  # Only max_concurrent requests at a time
            return await fetch_one(session, url)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example: Fetch multiple APIs concurrently."""
    urls = [
        "https://api.example.com/customers/123",
        "https://api.example.com/jobs/456",
        "https://api.example.com/techs/789",
        "https://weather.api.com/forecast",
    ]
    
    start = time.time()
    results = await fetch_all_bounded(urls, max_concurrent=4)
    elapsed = time.time() - start
    
    print(f"Fetched {len(results)} URLs in {elapsed:.2f}s")
    for r in results:
        print(f"  {r['url']}: {r['status']}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Complexity Analysis:**

| Approach | Time Complexity | When to Use |
|----------|----------------|-------------|
| Serial | O(n × avg_latency) | Never for I/O |
| `asyncio.gather()` | O(max_latency) | Small n, trusted server |
| `Semaphore(k)` | O(ceil(n/k) × avg_latency) | Large n, rate limiting needed |

---

## Pattern 3: LRU Cache

### Why This Matters at ServiceTitan

**Real-world use case:** Cache frequently accessed data to reduce database load:
- Customer details (accessed on every call)
- Technician schedules (checked for every dispatch)
- Pricing rules (used in every quote)

LRU (Least Recently Used) eviction ensures the cache stays bounded while keeping hot data.

### Problem: Implement LRU Cache

```python
from collections import OrderedDict
from typing import Optional

class LRUCache:
    """
    Least Recently Used cache with O(1) get and put.
    
    Uses OrderedDict which maintains insertion order and provides:
    - O(1) access by key (hash map)
    - O(1) move_to_end (doubly linked list)
    - O(1) popitem(last=False) to remove oldest
    
    Alternative: Implement your own doubly linked list + hash map
    (more code but shows you understand the data structure).
    """
    
    def __init__(self, capacity: int):
        """
        Initialize cache with fixed capacity.
        
        Args:
            capacity: Maximum number of items to store
        
        Raises:
            ValueError: If capacity <= 0
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache = OrderedDict()  # Maintains insertion order
    
    def get(self, key: int) -> int:
        """
        Get value for key, marking it as recently used.
        
        Time: O(1)
        Space: O(1)
        
        Returns:
            Value if key exists, -1 otherwise
        """
        if key not in self.cache:
            return -1
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        """
        Put key-value pair, evicting LRU item if at capacity.
        
        Time: O(1)
        Space: O(1)
        """
        if key in self.cache:
            # Update existing key and mark as recently used
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        # Evict least recently used if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest (first item)
    
    def __len__(self) -> int:
        """Return current cache size."""
        return len(self.cache)
    
    def __repr__(self) -> str:
        """Show cache contents in LRU order."""
        return f"LRUCache(capacity={self.capacity}, items={list(self.cache.items())})"


# ============================================================================
# TEST CASES
# ============================================================================

def test_lru_cache():
    """Test LRU cache behavior."""
    cache = LRUCache(capacity=2)
    
    # Test basic put/get
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1  # Returns 1
    
    # Test eviction (capacity=2, adding 3rd item evicts LRU)
    cache.put(3, 3)  # Evicts key 2 (least recently used)
    assert cache.get(2) == -1  # Key 2 was evicted
    
    # Test update existing key
    cache.put(1, 10)  # Update key 1
    assert cache.get(1) == 10
    
    # Test LRU ordering
    cache = LRUCache(capacity=3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    cache.get(1)  # Access 1 (now most recent)
    cache.put(4, 4)  # Should evict 2 (least recent)
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
    
    print("✓ LRU cache tests passed")


if __name__ == "__main__":
    test_lru_cache()
```

---

## Pattern 4: Priority Queue (Heap)

### Why This Matters at ServiceTitan

**Real-world use case:** Dispatch system prioritizes jobs by urgency and value:
- Emergency calls (highest priority)
- High-value customers (medium-high priority)
- Regular maintenance (normal priority)

### Problem: Job Scheduler with Priority

```python
import heapq
from typing import Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(order=True)
class Job:
    """
    Job with priority for scheduling.
    
    @dataclass(order=True) makes instances comparable by first field.
    We use negative priority for max-heap behavior (highest priority first).
    """
    priority: float = field(compare=True)  # Used for comparison
    timestamp: float = field(compare=True)  # Tie-breaker (FIFO for same priority)
    job_id: str = field(compare=False)  # Not used in comparison
    details: dict = field(compare=False, default_factory=dict)


class JobScheduler:
    """
    Priority queue for job scheduling using min-heap.
    
    Python's heapq is a min-heap, so we negate priorities for max-heap behavior.
    
    Time complexities:
    - push: O(log n)
    - pop: O(log n)
    - peek: O(1)
    """
    
    def __init__(self):
        self._heap = []
        self._counter = 0  # Monotonic counter for tie-breaking
    
    def push(self, job_id: str, priority: float, details: dict = None) -> None:
        """
        Add job to scheduler.
        
        Time: O(log n)
        Space: O(1)
        
        Args:
            job_id: Unique job identifier
            priority: Higher values = higher priority
            details: Optional job metadata
        """
        # Negate priority for max-heap (highest priority first)
        # Use counter for stable sort (FIFO for same priority)
        job = Job(
            priority=-priority,  # Negate for max-heap
            timestamp=self._counter,
            job_id=job_id,
            details=details or {}
        )
        heapq.heappush(self._heap, job)
        self._counter += 1
    
    def pop(self) -> Tuple[str, float, dict]:
        """
        Remove and return highest priority job.
        
        Time: O(log n)
        Space: O(1)
        
        Returns:
            (job_id, priority, details)
        
        Raises:
            IndexError: If scheduler is empty
        """
        if not self._heap:
            raise IndexError("pop from empty scheduler")
        
        job = heapq.heappop(self._heap)
        return (job.job_id, -job.priority, job.details)  # Un-negate priority
    
    def peek(self) -> Optional[Tuple[str, float, dict]]:
        """
        View highest priority job without removing.
        
        Time: O(1)
        Space: O(1)
        """
        if not self._heap:
            return None
        
        job = self._heap[0]
        return (job.job_id, -job.priority, job.details)
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return len(self._heap) > 0


# ============================================================================
# TEST CASES
# ============================================================================

def test_job_scheduler():
    """Test priority queue behavior."""
    scheduler = JobScheduler()
    
    # Add jobs with different priorities
    scheduler.push("job1", priority=5.0, details={"type": "maintenance"})
    scheduler.push("job2", priority=10.0, details={"type": "emergency"})
    scheduler.push("job3", priority=7.5, details={"type": "urgent"})
    
    # Should pop in priority order: 10.0, 7.5, 5.0
    job_id, priority, details = scheduler.pop()
    assert job_id == "job2" and priority == 10.0
    
    job_id, priority, details = scheduler.pop()
    assert job_id == "job3" and priority == 7.5
    
    job_id, priority, details = scheduler.pop()
    assert job_id == "job1" and priority == 5.0
    
    # Test FIFO for same priority
    scheduler.push("jobA", priority=5.0)
    scheduler.push("jobB", priority=5.0)
    scheduler.push("jobC", priority=5.0)
    
    assert scheduler.pop()[0] == "jobA"  # First in, first out
    assert scheduler.pop()[0] == "jobB"
    assert scheduler.pop()[0] == "jobC"
    
    print("✓ Job scheduler tests passed")


if __name__ == "__main__":
    test_job_scheduler()
```

---

## Interview Strategy & Tips

### Before You Start Coding

1. **Read the problem twice** - Make sure you understand all requirements
2. **Ask clarifying questions:**
   - "Should I handle None/null keys and values?"
   - "What should happen if capacity is 0?"
   - "Do I need to handle concurrent access?"
   - "Should keys be returned in any particular order?"

3. **State your approach:**
   - "I'll use a defaultdict(list) for O(1) put operations"
   - "I'll cache the size for O(1) queries"
   - "I'll use OrderedDict for O(1) LRU operations"

4. **Discuss complexity:**
   - "Put will be O(1) amortized, get will be O(n) for the copy"
   - "Overall space is O(N) where N is total pairs"

### While Coding

1. **Write clean code:**
   - Use meaningful variable names
   - Add docstrings with complexity analysis
   - Include type hints
   - Comment tricky parts

2. **Handle edge cases:**
   - Empty inputs
   - Capacity = 0 or 1
   - Duplicate values
   - None/null values
   - Very large inputs

3. **Test as you go:**
   - Write test cases
   - Run them to verify correctness
   - Test edge cases

### Common Mistakes to Avoid

❌ **Don't:**
- Start coding immediately without planning
- Ignore edge cases
- Forget to clean up empty keys (memory leak)
- Return references to internal data structures
- Forget to update cached counters
- Use O(n) operations when O(1) is possible

✅ **Do:**
- Explain your thinking out loud
- Mention tradeoffs ("I'm doing X instead of Y because...")
- Write test cases
- Ask if you're unsure about requirements
- Optimize after getting a working solution

### Time Management (90 minutes total)

- **Part 1 (30-40 min):**
  - 5 min: Read, understand, ask questions
  - 20 min: Implement basic solution
  - 10 min: Test and debug
  - 5 min: Add comments and cleanup

- **Part 2 (40-50 min):**
  - 5 min: Understand new requirements
  - 25 min: Implement optimizations
  - 15 min: Test thoroughly
  - 5 min: Final review

### What ServiceTitan Evaluates

| Criteria | Weight | What They Look For |
|----------|--------|-------------------|
| **Correctness** | 40% | Passes all test cases, handles edge cases |
| **Code Quality** | 25% | Clean, readable, well-structured |
| **Complexity** | 20% | Understands time/space tradeoffs |
| **Communication** | 15% | Explains decisions, asks good questions |

### Final Checklist Before Submitting

- [ ] All test cases pass
- [ ] Edge cases handled (empty, None, duplicates)
- [ ] Docstrings with complexity analysis
- [ ] Type hints on all methods
- [ ] No obvious bugs (off-by-one, null pointer, etc.)
- [ ] Code is readable and well-commented
- [ ] Tradeoffs are documented

---

## Additional Practice Problems

If you finish early or want more practice:

1. **Implement a Trie** - For autocomplete/search
2. **Design a Rate Limiter** - Token bucket or sliding window
3. **Implement a Bloom Filter** - Probabilistic set membership
4. **Design a Time-Series Database** - Store and query metrics
5. **Implement a Consistent Hash Ring** - For distributed caching

Good luck! 🚀

---

## Confirmed Interview Questions (From Glassdoor Reports)

### What's Actually Been Reported

This section is based on verified Glassdoor reviews and interview reports — not generic
prep guides. The distinction matters because ST's coding bar is pragmatic, not algorithmic.

**Confirmed problems (multiple reports):**
- **MultiMap / custom data structure implementation** — most commonly cited, already covered above
- **Subset sum / equal partition** — "given an array of unique integers, can it be split into two subsets with equal sums?" (LeetCode #416, DP)
- **Shallow and deep clone** — object graph traversal, copying nested structures without shared references
- **Incomplete instructions / hidden test cases** — multiple reviewers note you must reverse-engineer requirements from failing tests; edge case thinking > algorithm knowledge

**NOT confirmed for ServiceTitan specifically:**
- Palindrome problems — appear in generic ML interview guides but no ST-specific report
- Two-sum, sliding window, graph problems — common everywhere but not attributed to ST
- Tree/BST problems — no reports

**Tone from reviewers:**
> "Very pragmatic, study C# not algorithms"
> "HackerRank with test cases that don't fully describe the problem — you have to infer edge cases"
> "Part 1 was straightforward, Part 2 added a requirement that changed the whole approach"

---

## Pattern 4: Subset Sum / Equal Partition

### Why This Matters at ServiceTitan

Real-world analog: "Can these jobs be evenly distributed across two teams?" or
"Can this invoice be split into two equal batches?" — partition problems show up
in scheduling and billing contexts.

### Problem Statement

Given a list of unique positive integers, determine whether it can be partitioned
into two subsets with equal sums.

```
partition([1, 5, 11, 5])  → True   (subsets [1, 5, 5] and [11])
partition([1, 2, 3, 5])   → False  (no valid split)
partition([])              → True   (two empty subsets, both sum to 0)
partition([2])             → False  (can't split single element equally)
```

### Solution (Dynamic Programming)

Key insight: "can we partition into two equal halves?" is equivalent to
"does any subset sum to total/2?"

```python
def can_partition(nums: list[int]) -> bool:
    """
    Determine if nums can be split into two equal-sum subsets.
    
    Approach: reduce to subset-sum problem.
    If total is odd, impossible. Otherwise, find subset summing to total//2.
    
    dp[s] = True if some subset of nums sums to s.
    
    Time:  O(n * total)
    Space: O(total)
    """
    total = sum(nums)
    
    # Odd total: impossible to split equally
    if total % 2 != 0:
        return False
    
    target = total // 2
    
    # dp[s] = can we reach sum s using some subset?
    # Start: only sum 0 is reachable (empty subset)
    dp = {0}
    
    for num in nums:
        # For each reachable sum, adding num creates a new reachable sum
        # Iterate over a copy — don't modify set while iterating
        dp = dp | {s + num for s in dp}
        
        # Early exit: target already reachable
        if target in dp:
            return True
    
    return target in dp


# Tests
print(can_partition([1, 5, 11, 5]))   # True  — [1,5,5] and [11]
print(can_partition([1, 2, 3, 5]))    # False
print(can_partition([]))               # True  — two empty subsets
print(can_partition([2]))              # False
print(can_partition([2, 2]))           # True  — [2] and [2]
print(can_partition([100]))            # False
```

### Classic DP Array Version (what interviewers often expect)

```python
def can_partition_dp(nums: list[int]) -> bool:
    """
    Same logic using a boolean array instead of a set.
    Slightly more explicit — easier to explain step-by-step in an interview.
    
    Time:  O(n * target)
    Space: O(target)
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    
    target = total // 2
    
    # dp[s] = True if subset summing to s is achievable
    dp = [False] * (target + 1)
    dp[0] = True  # empty subset sums to 0
    
    for num in nums:
        # Iterate backwards to avoid using the same number twice
        # (this is a 0/1 knapsack — each number used at most once)
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]


print(can_partition_dp([1, 5, 11, 5]))   # True
print(can_partition_dp([1, 2, 3, 5]))    # False
```

---

## Pattern 5: Shallow and Deep Clone

### Why This Matters at ServiceTitan

Real-world analog: cloning a job record (with nested customer, equipment, line items)
without the copy sharing references with the original. Mutation of a "copied" job
should not affect the original.

This tests whether you understand Python's reference model — a common source of bugs
in data pipelines.

### The Problem with Shallow Copy

```python
import copy

# Shallow copy: top-level object is new, but nested objects are SHARED
original = {'job_type': 'ac_repair', 'parts': ['filter', 'refrigerant']}
shallow = original.copy()           # or copy.copy(original)

shallow['parts'].append('capacitor')  # modifies BOTH — shared reference!
print(original['parts'])  # ['filter', 'refrigerant', 'capacitor'] — BUG
```

### Shallow Clone Implementation

```python
def shallow_clone(obj):
    """
    Create a new object with the same top-level fields.
    Nested objects are NOT copied — both original and clone share them.
    
    Use when: top-level mutation is needed but nested data won't change.
    Time/Space: O(n) where n = number of top-level fields.
    """
    if isinstance(obj, dict):
        return dict(obj)          # new dict, same value references
    elif isinstance(obj, list):
        return list(obj)          # new list, same element references
    elif isinstance(obj, set):
        return set(obj)
    else:
        return obj                # primitives are immutable, no copy needed
```

### Deep Clone Implementation (the interview ask)

```python
def deep_clone(obj, memo=None):
    """
    Recursively copy an object and ALL nested objects.
    No reference sharing — mutation of clone never affects original.
    
    memo: dict tracking already-cloned objects to handle cycles.
    Without memo, a circular reference causes infinite recursion.
    
    Time:  O(n) where n = total number of objects in the graph
    Space: O(n) for memo dict + recursion stack depth
    """
    if memo is None:
        memo = {}
    
    # Check if we've already cloned this exact object (handle cycles)
    obj_id = id(obj)
    if obj_id in memo:
        return memo[obj_id]
    
    # Primitives and None are immutable — return as-is
    if obj is None or isinstance(obj, (int, float, str, bool)):
        return obj
    
    if isinstance(obj, dict):
        clone = {}
        memo[obj_id] = clone          # register BEFORE recursing (cycle safety)
        for key, val in obj.items():
            clone[deep_clone(key, memo)] = deep_clone(val, memo)
        return clone
    
    elif isinstance(obj, list):
        clone = []
        memo[obj_id] = clone          # register before recursing
        clone.extend(deep_clone(item, memo) for item in obj)
        return clone
    
    elif isinstance(obj, set):
        clone = set()
        memo[obj_id] = clone
        clone.update(deep_clone(item, memo) for item in obj)
        return clone
    
    elif isinstance(obj, tuple):
        # Tuples are immutable but may contain mutable objects
        clone = tuple(deep_clone(item, memo) for item in obj)
        memo[obj_id] = clone
        return clone
    
    else:
        # For custom objects: copy __dict__ recursively
        # In production: check for __deepcopy__ hook first
        import copy
        return copy.deepcopy(obj)     # fallback for complex types


# --- Tests ---
# Basic nested dict
job = {
    'job_type': 'ac_repair',
    'customer': {'name': 'Alice', 'address': '123 Main'},
    'parts': ['filter', 'refrigerant'],
}
cloned = deep_clone(job)
cloned['customer']['name'] = 'Bob'      # mutate clone
cloned['parts'].append('capacitor')
print("original customer:", job['customer']['name'])   # Alice — unchanged
print("original parts:", job['parts'])                  # ['filter', 'refrigerant']

# Cycle handling
a = {'val': 1}
b = {'val': 2, 'partner': a}
a['partner'] = b                        # a -> b -> a (cycle)
a_clone = deep_clone(a)
print("cycle clone val:", a_clone['val'])               # 1
print("cycle preserved:", a_clone['partner']['partner'] is a_clone)  # True
```

---

## Pattern 6: Inferring Requirements from Hidden Test Cases

This is the most reported differentiator in ST HackerRank reviews. The problem statement
is intentionally underspecified — you must write defensive code that handles cases the
prompt doesn't mention.

### Common hidden edge cases by problem type

**Any data structure (MultiMap, LRU, etc.):**
- `get()` on a key that was never inserted
- `remove()` on a key/value that doesn't exist
- `put()` with `None` as key or value
- Operations on a just-constructed (empty) instance
- Duplicate `put()` calls with the same key AND value

**Subset sum / partition:**
- Empty list `[]`
- Single element `[x]`
- All elements identical `[2, 2, 2, 2]`
- Total is odd (fast return False)
- Very large values (int overflow is not a Python concern, but mention it)

**Clone:**
- `None` input
- Circular references (the memo pattern above handles this)
- Object containing a mix of types (int, str, list, dict nested together)
- Empty collections `{}`, `[]`, `set()`

### Strategy: write your own tests before submitting

```python
# Template: always run these before hitting Submit
def run_edge_cases(fn, cases):
    for inputs, expected, label in cases:
        result = fn(*inputs) if isinstance(inputs, tuple) else fn(inputs)
        status = "PASS" if result == expected else f"FAIL (got {result})"
        print(f"  [{status}] {label}")

# Example for can_partition:
run_edge_cases(can_partition, [
    (([],),        True,  "empty list"),
    (([2],),       False, "single element"),
    (([2, 2],),    True,  "two equal elements"),
    (([1,2,3,5],), False, "no valid partition"),
    (([1,5,11,5],),True,  "valid partition"),
])
```
