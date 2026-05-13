"""
VersionedMultiMap - A multimap with full version history for time-travel queries.

Use case: Customer tags, job attachments, audit trails where you need to answer
"What values existed for this key at timestamp X?"
"""

from collections import defaultdict
from typing import Any, List, Tuple


class VersionedMultiMap:
    """Key -> list of values, with version-stamped history per key.
    
    A multimap allows multiple values per key (unlike a regular dict).
    The versioned aspect means we can query historical state at any past version.
    
    Example:
        m = VersionedMultiMap()
        v1 = m.add("customer_1", "vip")          # version 1
        v2 = m.add("customer_1", "high_value")   # version 2
        v3 = m.remove("customer_1", "vip")       # version 3
        
        m.get("customer_1")              # ["high_value"] (current state)
        m.get_at("customer_1", 2)        # ["vip", "high_value"] (historical)
    """

    def __init__(self) -> None:
        """Initialize empty multimap with version tracking."""
        # Current state: key -> list of values
        self._current: dict[Any, list[Any]] = defaultdict(list)
        
        # History log: key -> list of (version, operation, value) tuples
        # Used for time-travel queries via get_at()
        self._log: dict[Any, list[Tuple[int, str, Any]]] = defaultdict(list)
        
        # Global version counter - increments on every add/remove
        self._version: int = 0
        
        # Total count of current key-value pairs (not unique keys)
        self._size: int = 0

    def add(self, key: Any, value: Any) -> int:
        """Add a value to the key's list.
        
        Args:
            key: The key to add the value under
            value: The value to append (duplicates are allowed)
            
        Returns:
            The new global version number after this operation
            
        Example:
            m.add("customer_1", "vip")     # Returns 1
            m.add("customer_1", "loyal")   # Returns 2
        """
        # Increment global version counter for this mutation
        self._version += 1
        
        # Append to current state (allows duplicates)
        self._current[key].append(value)
        
        # Log this operation for historical queries
        self._log[key].append((self._version, "add", value))
        
        # Track total pair count
        self._size += 1
        
        return self._version

    def remove(self, key: Any, value: Any) -> int:
        """Remove first occurrence of value from key's list.
        
        Args:
            key: The key to remove the value from
            value: The value to remove (only first occurrence)
            
        Returns:
            The new global version number after this operation
            
        Raises:
            KeyError: If value is not in key's list
            
        Example:
            m.add("k", "v")
            m.add("k", "v")      # Duplicate
            m.remove("k", "v")   # Removes first "v", one remains
        """
        # Validate value exists before removing
        if value not in self._current[key]:
            raise KeyError(f"value {value!r} not in key {key!r}")
        
        # Increment version for this mutation
        self._version += 1
        
        # Remove first occurrence from current state
        self._current[key].remove(value)
        
        # Log the removal operation
        self._log[key].append((self._version, "remove", value))
        
        # Decrement pair count
        self._size -= 1
        
        return self._version

    def get(self, key: Any) -> List[Any]:
        """Get current values for a key.
        
        Args:
            key: The key to look up
            
        Returns:
            List of current values (empty list if key doesn't exist)
            Returns a copy to prevent external mutation
            
        Example:
            m.add("k", "a")
            m.add("k", "b")
            m.get("k")  # ["a", "b"]
            m.get("unknown")  # []
        """
        # Return copy to prevent external mutation of internal state
        return list(self._current[key])

    def get_at(self, key: Any, version: int) -> List[Any]:
        """Get historical values for a key at a specific version (time-travel query).
        
        Reconstructs what the key's values were after the specified version
        by replaying the log up to that point.
        
        Args:
            key: The key to look up
            version: The version number to query (0 = before any operations)
            
        Returns:
            List of values that existed at that version
            
        Example:
            m.add("k", "v1")     # version 1
            m.add("k", "v2")     # version 2
            m.remove("k", "v1")  # version 3
            
            m.get_at("k", 0)  # []
            m.get_at("k", 1)  # ["v1"]
            m.get_at("k", 2)  # ["v1", "v2"]
            m.get_at("k", 3)  # ["v2"]
        """
        # Start with empty state and replay history
        state: list[Any] = []
        
        # Process each logged operation up to target version
        for v, op, val in self._log[key]:
            # Stop when we've passed the target version
            if v > version:
                break
            
            # Apply the operation to reconstruct state
            if op == "add":
                state.append(val)
            else:  # op == "remove"
                state.remove(val)  # Removes first occurrence
        
        return state

    def size(self) -> int:
        """Get total count of current key-value pairs.
        
        Note: This counts pairs, not unique keys.
        
        Returns:
            Total number of key-value pairs currently stored
            
        Example:
            m.add("k1", "v1")
            m.add("k1", "v2")
            m.add("k2", "v3")
            m.size()  # 3 (not 2)
        """
        return self._size

    def __repr__(self) -> str:
        """Return debug representation showing current version and size."""
        return f"VersionedMultiMap(v={self._version}, size={self._size})"
