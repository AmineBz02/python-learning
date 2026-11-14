# 🎫 Backlog — Student Grade Manager (MVP)

**Format:** Jira-style issues with ID, type, summary, description, acceptance criteria (AC), estimate, priority, dependencies.

**Epic:** `SGM-0` — Student Grade Manager (MVP)
**Story Points scale:** 1 (trivial) · 2 (small) · 3 (medium) · 5 (large) · 8 (too big, split)

---

## Epic

| Field | Value |
|-------|-------|
| **ID** | SGM-0 |
| **Type** | Epic |
| **Summary** | Student Grade Manager — MVP CLI |
| **Description** | Single-file Python CLI to add students/scores, compute averages, find top student, show a report, and persist to `students.txt`. |
| **Priority** | High |
| **Labels** | `level-2`, `mvp`, `cli`, `python` |
| **Definition of Done (Epic)** | All child stories closed; full flow works; no crashes on bad input; save/load round-trip works. |

---

## Stories

---

### SGM-1 — Project skeleton & entry point
| Field | Value |
|-------|-------|
| **Type** | Task |
| **Priority** | Highest |
| **Estimate** | 1 |
| **Labels** | `setup` |
| **Depends on** | — |

**Description**
Create the single-file app with a `main()` function and entry-point guard.

**Tasks**
- Create `student_grade_manager.py`.
- Add `def main() -> None:` printing a placeholder.
- Add `if __name__ == "__main__": main()`.

**AC**
- [ ] Script runs with `python student_grade_manager.py`.
- [ ] Prints a placeholder message.
- [ ] No errors/warnings.

---

### SGM-2 — `add_student(name)`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | Highest |
| **Estimate** | 2 |
| **Labels** | `feature`, `core` |
| **Depends on** | SGM-1 |

**Description**
Add a student to the `students` dict with an empty score list. Reject duplicates and empty names.

**AC**
- [ ] `add_student(students, "Ali")` → `students == {"Ali": []}`.
- [ ] Adding `"Ali"` again prints a message and does not overwrite.
- [ ] Empty/whitespace-only name is rejected with a message.
- [ ] Name is stripped of surrounding whitespace before storage.

---

### SGM-3 — `add_score(name, score)`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | Highest |
| **Estimate** | 2 |
| **Labels** | `feature`, `core`, `validation` |
| **Depends on** | SGM-2 |

**Description**
Append a validated score to an existing student's list.

**AC**
- [ ] Valid score (0–100) is appended to the correct student's list.
- [ ] Missing student → message, no change.
- [ ] Non-numeric input → message, no change (no exception leaks).
- [ ] Score < 0 or > 100 → message, no change.
- [ ] Other students' data is unaffected.

---

### SGM-4 — `average(name)`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | High |
| **Estimate** | 1 |
| **Labels** | `feature`, `calc` |
| **Depends on** | SGM-3 |

**Description**
Return the mean of a student's scores.

**AC**
- [ ] Returns correct float for a student with scores (e.g. `[90,85,70]` → `81.666…`).
- [ ] Returns `None` if student is missing.
- [ ] Returns `None` if the student has no scores.
- [ ] Does not mutate the dict.

---

### SGM-5 — `top_student()`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | High |
| **Estimate** | 2 |
| **Labels** | `feature`, `calc` |
| **Depends on** | SGM-4 |

**Description**
Return the name of the student with the highest average.

**AC**
- [ ] Returns the correct name for 3 students with distinct averages.
- [ ] Students with no scores are ignored.
- [ ] Returns `None` if the dict is empty.
- [ ] Returns `None` if no student has any scores.
- [ ] Tie-break rule documented (MVP: first inserted wins — dict order).

---

### SGM-6 — `show_report()`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | High |
| **Estimate** | 3 |
| **Labels** | `feature`, `ui` |
| **Depends on** | SGM-4 |

**Description**
Print an aligned table: `Name | Scores | Average`.

**AC**
- [ ] Header row prints exactly once.
- [ ] Columns are aligned using f-string padding.
- [ ] Average shown with 2 decimals (or `N/A` if none).
- [ ] Empty `students` → prints `No students yet` and exits cleanly.
- [ ] Report matches the dict contents (no extra/missing rows).

---

### SGM-7 — `save_to_file(path="students.txt")`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | High |
| **Estimate** | 2 |
| **Labels** | `feature`, `persistence` |
| **Depends on** | SGM-2, SGM-3 |

**Description**
Persist the `students` dict to a `.txt` file.

**AC**
- [ ] Uses `with open(path, "w")`.
- [ ] Format: one line per student, `Name: s1,s2,s3`.
- [ ] Empty dict → writes an empty (or header-less) file without error.
- [ ] Overwrites existing file (no append).
- [ ] Round-trip with SGM-8 preserves values.

---

### SGM-8 — `load_from_file(path="students.txt")`
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | High |
| **Estimate** | 3 |
| **Labels** | `feature`, `persistence` |
| **Depends on** | SGM-7 |

**Description**
Parse the `.txt` file back into the `students` dict.

**AC**
- [ ] Uses `with open(path, "r")`.
- [ ] Missing file → prints a message, returns `{}`, no crash.
- [ ] Parses `Name: 90,85,70` → `{"Name": [90.0, 85.0, 70.0]}`.
- [ ] Empty score list (`Name:`) parses to `[]`.
- [ ] Malformed line is skipped (MVP: warn and continue).
- [ ] Save → load round-trip equals original dict.

---

### SGM-9 — Interactive menu loop
| Field | Value |
|-------|-------|
| **Type** | Story |
| **Priority** | Highest |
| **Estimate** | 3 |
| **Labels** | `feature`, `cli`, `integration` |
| **Depends on** | SGM-2 … SGM-8 |

**Description**
Wire all functions into a `main()` menu loop.

**Tasks**
- Print menu: `1) Add student  2) Add score  3) Average  4) Top student  5) Show report  6) Save  7) Load  8) Exit`.
- Read choice; dispatch to the matching function.
- Validate menu choice; unknown → message, re-loop.

**AC**
- [ ] All 8 options invoke the correct function.
- [ ] Exit option breaks the loop cleanly.
- [ ] Invalid menu choice → message, loop continues.
- [ ] Score input parsed with `try/except ValueError`.
- [ ] End-to-end flow 1 → 2 → 5 → 6 → 8 succeeds without crashes.

---

## Bug / Hardening (post-MVP polish, optional)

### SGM-10 — Manual test pass & edge-case hardening
| Field | Value |
|-------|-------|
| **Type** | Task |
| **Priority** | Medium |
| **Estimate** | 2 |
| **Labels** | `qa` |
| **Depends on** | SGM-9 |

**Description**
Run the LLD testing checklist (12 cases) and fix any leaks.

**AC**
- [ ] All 12 checklist items from LLD §4.5 pass.
- [ ] No unhandled exceptions on any input path.
- [ ] No functional change beyond bug fixes.

---

## Backlog Board (suggested order)

```
TODO        | SGM-1
IN PROGRESS |
DONE        |
```

**Sequence:** `SGM-1 → SGM-2 → SGM-3 → SGM-4 → SGM-5 → SGM-6 → SGM-7 → SGM-8 → SGM-9 → SGM-10`

---

## Summary Table

| ID | Type | Summary | Est | Priority | Depends on |
|----|------|---------|-----|----------|------------|
| SGM-0 | Epic | Student Grade Manager MVP | — | High | — |
| SGM-1 | Task | Project skeleton & entry point | 1 | Highest | — |
| SGM-2 | Story | `add_student(name)` | 2 | Highest | SGM-1 |
| SGM-3 | Story | `add_score(name, score)` | 2 | Highest | SGM-2 |
| SGM-4 | Story | `average(name)` | 1 | High | SGM-3 |
| SGM-5 | Story | `top_student()` | 2 | High | SGM-4 |
| SGM-6 | Story | `show_report()` | 3 | High | SGM-4 |
| SGM-7 | Story | `save_to_file()` | 2 | High | SGM-2,3 |
| SGM-8 | Story | `load_from_file()` | 3 | High | SGM-7 |
| SGM-9 | Story | Interactive menu loop | 3 | Highest | SGM-2…8 |
| SGM-10 | Task | Manual test pass | 2 | Medium | SGM-9 |

**Total:** 10 issues (1 epic + 9 work items), **~21 points**, single sprint.

---

Want this as a **CSV / Jira-import JSON** next, or the same backlog pack for **Level 3 (Expense Tracker)**?