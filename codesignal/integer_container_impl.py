from statistics import mean
import sys
import os
import numpy as np
# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from integer_container import IntegerContainer

class IntegerContainerImpl(IntegerContainer):
    def __init__(self):
        # You can change this later if you want better performance
        self.integers = []
        self.history = [] # format: action, timestamp, value
        
    # ----- Level 1 -----
    def add(self, value: int) -> int:
        self.integers.append(value)
        return len(self.integers)

    def delete(self, value: int) -> bool:
        if value in self.integers:
            self.integers.remove(value)
            return True
        return False

    # ----- Level 2 -----
    def get_median(self) -> int | None:
        # if even:
        if not self.integers:
            return None
        l = len(self.integers)
        intsort = sorted(self.integers)
        if l % 2 == 0: 
            med = intsort[l // 2 - 1]
        else: 
            med = intsort[l // 2]
            
        return med

    # ----- Level 3 -----
    def add_all(self, values: list[int]) -> int:
        for val in values:
            self.integers.append(val)
        return len(self.integers)

    def delete_all(self, value: int) -> int:
        self.integers = [x for x in self.integers if x != value] # overwrites list 
        return self.integers

    def get_min(self) -> int | None:
        return min(self.integers)

    def get_max(self) -> int | None:
        return max(self.integers)

    def get_mean(self) -> float | None:
        return mean(self.integers)

    # ----- Level 4 -----
    def add_at(self, timestamp: int, value: int) -> int:
        self.integers.append(value)
        self.history.append(['add_at', timestamp, value])
        return len(self.integers)

    def delete_at(self, timestamp: int, value: int) -> bool:
        if value in self.integers:
            self.integers.remove(value)
            self.history.append(['delete_at', timestamp, value])
            return True
        return False

    def rollback(self, timestamp: int) -> None:
        # rebuild the full set from the kept history;
        kept = []
        for event in self.history: #history from start to finish
            if event[1] <= timestamp: # if timestamp of a historical event is before rollback date
                kept.append(event)
        
        # rebuild
        int2 = []
        for event in kept: # rebuild from start to finish
            if event[0] == 'add_at':
                int2.append(event[2])
            elif event[0] == 'delete_at':
                int2.remove(event[2]) #value 
            else: 
                raise RuntimeError("unknown command - rolling back failed")
            
        self.integers = int2
        pass

    def percentile(self, p: float) -> int | None:
        return np.percentile(self.integers, p)
