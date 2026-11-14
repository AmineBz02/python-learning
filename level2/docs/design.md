# 📄 Student Grade Manager — MVP Docs

---

## 1. PRD (Product Requirements Document)

**Product:** Student Grade Manager (CLI)
**Version:** MVP 1.0
**Owner:** Learner (Level 2 Python path)

### 1.1 Problem
A beginner needs a small tool to practice core data structures (dicts/lists), functions, and file I/O — while actually managing student scores.

### 1.2 Goal
A single-file CLI script that stores students and scores, computes averages, shows a report, and persists data to a `.txt` file.

### 1.3 Users
Single user (the learner), running locally from a terminal.

### 1.4 In-Scope Features (MVP)
| # | Feature | Priority |
|---|---------|----------|
| F1 | Add student | Must |
| F2 | Add score (validated 0–100) | Must |
| F3 | Compute average per student | Must |
| F4 | Find top student | Must |
| F5 | Formatted report table | Must |
| F6 | Save to `.txt` | Must |
| F7 | Load from `.txt` | Must |
| F8 | Interactive menu loop | Must |

### 1.5 Out of Scope
JSON/CSV, `*args`/`**kwargs` demos, GUI, database, multi-class OOP, editing/deleting students, sorting/filtering.

### 1.6 Success Criteria
- Full flow (add → score → report → save → load → exit) works without crashing.
- Bad input (missing student, non-numeric score, missing file) is handled gracefully.
- Save/load round-trip produces identical data.

### 1.7 Non-Functional (light)
- Single file, stdlib only, runs on Python 3.10+.
- No external dependencies.

---

## 2. SRS (Software Requirements Specification)

### 2.1 Functional Requirements
| ID | Requirement |
|----|-------------|
| FR-1 | System shall add a student by name; duplicate names are rejected with a message. |
| FR-2 | System shall add a numeric score (0–100) to an existing student; non-numeric or out-of-range input is rejected with a message. |
| FR-3 | System shall compute and return a student's average; returns `None` if student missing or has no scores. |
| FR-4 | System shall return the name of the student with the highest average; returns `None` if no students. |
| FR-5 | System shall print a report with columns `Name | Scores | Average`, aligned. |
| FR-6 | System shall save data to a text file in format `Name: s1,s2,s3` (one student per line). |
| FR-7 | System shall load data from that file; if the file is missing, print a message and continue. |
| FR-8 | System shall provide a menu loop with options 1–8 (Add student, Add score, Average, Top student, Show report, Save, Load, Exit). |

### 2.2 Non-Functional Requirements
| ID | Requirement |
|----|-------------|
| NFR-1 | Python 3.10+, standard library only. |
| NFR-2 | Single file `student_grade_manager.py`. |
| NFR-3 | No unhandled exceptions on any user input. |
| NFR-4 | Functions are small (< ~20 lines) and single-purpose. |
| NFR-5 | Data persists across runs via save/load. |

### 2.3 Constraints
- File-based storage only (no DB).
- CLI only (no GUI/web).

### 2.4 Assumptions
- User runs the script manually.
- Data file path is provided by the user or defaulted to `students.txt`.

---

## 3. HLD (High-Level Design)

### 3.1 Architecture
Single-file, function-based (procedural) CLI app.

```
┌─────────────────────────────┐
│         main()              │  ← menu loop
│  (reads choice, dispatches) │
└──────────────┬──────────────┘
               │ calls
   ┌───────────┼───────────┬────────────┬────────────┐
   ▼           ▼           ▼            ▼            ▼
add_student add_score   average    top_student   show_report
                                                   │
                                          save_to_file / load_from_file
                                                   │
                                                   ▼
                                             students.txt
```

### 3.2 Data Model
```python
students: dict[str, list[float]] = {
    "Ali":  [90, 85, 70],
    "Sara": [100, 95],
}
```

### 3.3 Module Responsibilities
| Component | Responsibility |
|-----------|----------------|
| `main()` | Menu loop, input parsing, dispatch |
| `add_student` | Insert new key, reject duplicates |
| `add_score` | Validate + append score |
| `average` | Compute mean, handle edge cases |
| `top_student` | Max by average |
| `show_report` | Format + print table |
| `save_to_file` / `load_from_file` | Persistence (`.txt`) |

### 3.4 Data Flow
1. `main()` reads menu choice.
2. Dispatches to function with `students` dict.
3. Functions mutate or read the dict.
4. Save/load serialize/deserialize to `students.txt`.

### 3.5 Error Handling Strategy
- Missing student → print message, return.
- Bad score → print message, return.
- Missing file → print message, return.
- No `try/except` needed beyond `FileNotFoundError` and `ValueError` (Level 3 deepens this).

### 3.6 File Format
```
Ali: 90,85,70
Sara: 100,95
```

---

## 4. LLD (Low-Level Design)

### 4.1 Function Signatures
```python
def add_student(students: dict, name: str) -> None
def add_score(students: dict, name: str, score: float) -> None
def average(students: dict, name: str) -> float | None
def top_student(students: dict) -> str | None
def show_report(students: dict) -> None
def save_to_file(students: dict, path: str = "students.txt") -> None
def load_from_file(path: str = "students.txt") -> dict
def main() -> None
```

### 4.2 Function Logic (pseudocode)

**add_student**
```
if name in students: print "already exists"; return
students[name] = []
```

**add_score**
```
if name not in students: print "not found"; return
if not 0 <= score <= 100: print "invalid score"; return
students[name].append(score)
```

**average**
```
if name not in students or not students[name]: return None
return sum(scores) / len(scores)
```

**top_student**
```
if not students: return None
return max(students, key=lambda n: sum(students[n])/len(students[n]) if students[n] else -1)
```

**show_report**
```
print header
for name, scores in students.items():
    avg = average(...) or "N/A"
    print f"{name:<12} {str(scores):<20} {avg}"
```

**save_to_file**
```
with open(path, "w") as f:
    for name, scores in students.items():
        f.write(f"{name}: {','.join(map(str, scores))}\n")
```

**load_from_file**
```
try: open(path)
except FileNotFoundError: print "no file"; return {}
parse each line "Name: s1,s2,s3" → dict
```

**main (menu loop)**
```
students = {}
while True:
    print menu 1–8
    choice = input()
    if choice == "8": break
    elif choice == "1": name = input(); add_student(students, name)
    elif choice == "2": name, score = ...; add_score(...)
    elif choice == "3": print(average(...))
    elif choice == "4": print(top_student(...))
    elif choice == "5": show_report(...)
    elif choice == "6": save_to_file(students)
    elif choice == "7": students = load_from_file()
    else: print "invalid"
```

### 4.3 Input Parsing Rules
- Score: `float(input())` wrapped in `try/except ValueError` → print "invalid number".
- Name: strip whitespace; reject empty string.

### 4.4 Edge Cases
| Case | Behavior |
|------|----------|
| Duplicate student | Message, no change |
| Score on missing student | Message, no change |
| Non-numeric score | Message, no change |
| Score out of 0–100 | Message, no change |
| Empty students on report | Print "No students yet" |
| `top_student` on empty | Returns `None` |
| Load missing file | Message, keep current dict (or `{}`) |
| Malformed line in file | Skip line (MVP: ignore silently or print warning) |

### 4.5 Testing Checklist (manual, MVP)
1. Add "Ali" → exists.
2. Add "Ali" again → rejected.
3. Add scores 90, 85, 70 to Ali → list correct.
4. Add score 150 → rejected.
5. Add score "abc" → rejected.
6. Average of Ali → 81.67.
7. Add Sara 100, 95 → `top_student` = Sara.
8. Report prints aligned table.
9. Save → file contents match format.
10. Load → dict identical.
11. Load with missing file → no crash.
12. Full menu flow 1→2→5→6→8 works.

---

## 📁 Deliverables Summary
- `student_grade_manager.py` (single file)
- `students.txt` (generated at runtime)
- This doc set (PRD/SRS/HLD/LLD)

**Out of scope:** JSON, OOP, DB, tests folder, packaging, CI.

--