import typing as tp

class DatabaseImpl:
    """
    An in-memory key-value database that supports time-to-live (TTL) features.
    """

    def __init__(self):
        """
        Initializes the database.
        The data is stored in a nested dictionary structure:
        {
            "key1": {
                "field1": (value, creation_timestamp, ttl),
                "field2": (value, creation_timestamp, ttl),
            },
            ...
        }
        """
        self.db: tp.Dict[str, tp.Dict[str, tp.Tuple[str, int, float]]] = {}

    def _is_expired(self, value_info: tp.Tuple[str, int, float], current_timestamp: int) -> bool:
        """
        Helper function to check if a record is expired at a given timestamp.
        A record expires if current_timestamp >= creation_timestamp + ttl.
        """
        _, creation_ts, ttl = value_info
        return current_timestamp >= creation_ts + ttl

    # --------------------------------------------------------------------------
    # Level 1 & 3: SET, GET, DELETE Methods
    # --------------------------------------------------------------------------

    def set(self, key: str, field: str, value: str) -> str:
        """Level 1: Sets a value. Backward compatible, assumes timestamp=0."""
        return self.set_at(key, field, value, 0)

    def set_at(self, key: str, field: str, value: str, timestamp: int) -> str:
        """Level 3: Sets a value at a specific timestamp with infinite TTL."""
        # An infinite TTL is represented by float('inf').
        return self.set_at_with_ttl(key, field, value, timestamp, float('inf'))

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> str:
        """Level 3: Sets a value with a creation timestamp and a TTL."""
        if key not in self.db:
            self.db[key] = {}
        self.db[key][field] = (value, int(timestamp), float(ttl))
        return ""

    def get(self, key: str, field: str) -> str:
        """Level 1: Gets a value. Backward compatible, assumes timestamp=0."""
        return self.get_at(key, field, 0)

    def get_at(self, key: str, field: str, timestamp: int) -> str:
        """Level 3: Gets a value at a specific timestamp, respecting TTL."""
        if key not in self.db or field not in self.db[key]:
            return ""

        value_info = self.db[key][field]
        if self._is_expired(value_info, int(timestamp)):
            return ""

        return value_info[0]

    def delete(self, key: str, field: str) -> str:
        """Level 1: Deletes a value. Backward compatible, assumes timestamp=0."""
        return self.delete_at(key, field, 0)

    def delete_at(self, key: str, field: str, timestamp: int) -> str:
        """Level 3: Deletes a value at a specific timestamp, respecting TTL."""
        if key not in self.db or field not in self.db[key]:
            return "false"

        value_info = self.db[key][field]
        if self._is_expired(value_info, int(timestamp)):
            # Cannot delete an already-expired record
            return "false"

        del self.db[key][field]
        return "true"

    # --------------------------------------------------------------------------
    # Level 2 & 3: SCAN Methods
    # --------------------------------------------------------------------------

    def scan(self, key: str) -> str:
        """Level 2: Scans all records for a key. Assumes timestamp=0."""
        return self.scan_at(key, 0)

    def scan_at(self, key: str, timestamp: int) -> str:
        """Level 3: Scans all non-expired records for a key at a given timestamp."""
        if key not in self.db:
            return ""

        records = []
        # Sort by field name alphabetically
        for field, value_info in sorted(self.db[key].items()):
            if not self._is_expired(value_info, int(timestamp)):
                value = value_info[0]
                records.append(f"{field}({value})")

        return ", ".join(records)

    def scan_by_prefix(self, key: str, prefix: str) -> str:
        """Level 2: Scans records matching a prefix. Assumes timestamp=0."""
        return self.scan_by_prefix_at(key, prefix, 0)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> str:
        """Level 3: Scans non-expired records matching a prefix at a given timestamp."""
        if key not in self.db:
            return ""

        records = []
        # Sort by field name alphabetically
        for field, value_info in sorted(self.db[key].items()):
            if field.startswith(prefix):
                if not self._is_expired(value_info, int(timestamp)):
                    value = value_info[0]
                    records.append(f"{field}({value})")

        return ", ".join(records)
