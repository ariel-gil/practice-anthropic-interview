

# Integer Container – Practice Project

This project is a **progressive coding exercise** based on the CodeSignal / Industry Coding Framework.
It implements a container of integers with increasing functionality across **4 levels**.
Each level builds on the previous one — you should refactor rather than rewrite.

---

## 📊 Levels & Requirements

### **Level 1 – Basic Functions**

Implement the fundamentals:

* `add(value: int) -> int`
  Add the integer to the container and return the number of integers stored after addition.
* `delete(value: int) -> bool`
  Remove one occurrence of the integer if it exists. Return `True` if removed, `False` otherwise.

Focus: **basic data structure handling** (list, array, etc.).

---

### **Level 2 – Median**

Add statistical querying:

* `get_median() -> int | None`
  Return the median integer (sorted order).

  * If count is odd → middle element.
  * If count is even → return the **leftmost** of the two middle elements.
  * If empty → return `None`.

Focus: **data processing** on top of Level 1 methods.

---

### **Level 3 – Refactoring & Encapsulation**

Extend design with helper methods and refactor for reusability:

* `add_all(values: list[int]) -> int`
  Add multiple integers at once. Return total count afterwards.
* `delete_all(value: int) -> int`
  Remove all occurrences of the given value. Return number removed.
* `get_min() -> int | None`
  Return the smallest integer, or `None` if empty.
* `get_max() -> int | None`
  Return the largest integer, or `None` if empty.
* `get_mean() -> float | None`
  Return the arithmetic mean, or `None` if empty.

Focus: **refactoring and code reuse**. If you’ve designed Level 1 & 2 efficiently, adding these should be easy.

---

### **Level 4 – Extending Design & Functionality**

Introduce **time-aware operations** and more advanced queries:

* `add_at(timestamp: int, value: int) -> int`
  Add a value at a specific timestamp.
* `delete_at(timestamp: int, value: int) -> bool`
  Delete a value at a specific timestamp.
* `rollback(timestamp: int) -> None`
  Restore the container to the state it had at that timestamp.
* `percentile(p: float) -> int | None`
  Return the *p*-th percentile value (0 ≤ p ≤ 100). Return `None` if empty.

Focus: **scalability and backward compatibility**.
Efficient design (e.g. using sorted structures, heaps, or logs) will help handle these new features.

---

## 🧪 Testing

Tests are provided in `test_integer_container.py`.
Run them with:

```bash
pytest
```

or

```bash
python -m pytest
```

---

## 🗂 File Structure

```
.
├── integer_container.py        # Interface definition (levels 1–4 methods)
├── integer_container_impl.py   # Concrete class with stubs → implement here
├── test_integer_container.py   # Unit tests (pytest style)
└── README.md                   # This file
```

---

🚀 **Goal**: Progress through the levels, refactoring as needed.
This simulates real-world coding where requirements grow and design decisions early on affect later complexity.

---

Would you like me to also add a **scoring guide** (like “Level 1 complete = 200 pts, Level 2 = 300 pts…” similar to the framework PDF), or keep it requirements-only?
