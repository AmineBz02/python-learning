DEFAULT_PATH = "students.txt"



def add_student(students: dict, name: str) -> None:
   if name.strip() == "":
      print("Error: Student name cannot be empty.")
      return
   if name in students:
      print(f"Error: Student '{name}' already exists.")
      return
   students[name] = []
def add_score(students: dict, name: str, score: float) -> None:
   if name not in students:
      print(f"Error: Student '{name}' does not exist.")
      return
   if not isinstance(score, (int, float)):
      print("Error: Score must be a number.")
      return
   if score < 0 or score > 100:
      print("Error: Score must be between 0 and 100.")
      return
   students[name].append(score)

def average(students: dict, name: str) -> float | None:
   if name not in students:
      print(f"Error: Student '{name}' does not exist.")
      return None
   if not students[name]:
      print(f"Error: Student '{name}' has no scores.")
      return None
   return sum(students[name]) / len(students[name])

def top_student(students: dict) -> str | None:
   if not students:
      print("Error: No students available.")
      return None 
   
   return max(students, key=lambda n: sum(students[n])/len(students[n]) if students[n] else -1)

# ═════════════════════════════════════════════════════════════
# SGM-6 — show_report()
# ═════════════════════════════════════════════════════════════
def show_report(students: dict[str, list[float]]) -> None:
    """Print an aligned table: Name | Scores | Average."""
    if not students:
        print("No students yet")
        return

    # Auto-fit column widths from data (f-string padding)
    name_w = max(len("Name"), *(len(n) for n in students))
    scores_w = max(
        len("Scores"),
        *(len(", ".join(f"{x:g}" for x in s)) if s else len("[]")
          for s in students.values()),
    )

    header = f"{'Name':<{name_w}} | {'Scores':<{scores_w}} | Average"
    print(header)
    print("-" * len(header))  # header printed exactly once above

    for name, scores in students.items():
        scores_str = ", ".join(f"{x:g}" for x in scores) if scores else "[]"
        avg = average(students, name)
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        print(f"{name:<{name_w}} | {scores_str:<{scores_w}} | {avg_str}")
# ═════════════════════════════════════════════════════════════
# SGM-7 — save_to_file()
# ═════════════════════════════════════════════════════════════
def save_to_file(students: dict[str, list[float]],
                 path: str = DEFAULT_PATH) -> None:
    """Persist to text file: one line per student as 'Name: s1,s2,s3'."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            for name, scores in students.items():
                f.write(f"{name}: {','.join(f'{x:g}' for x in scores)}\n")
        print(f"💾 Saved {len(students)} student(s) to '{path}'.")
    except OSError as e:
        print(f"⚠️  Could not save to '{path}': {e}")

# ═════════════════════════════════════════════════════════════
# SGM-8 — load_from_file()
# ═════════════════════════════════════════════════════════════
def load_from_file(path: str = DEFAULT_PATH) -> dict[str, list[float]]:
    """Parse text file back into dict. Missing file → {} (no crash)."""
    students: dict[str, list[float]] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line:
                    continue
                if ":" not in line:
                    print(f"⚠️  Skipping malformed line {lineno}: {line!r}")
                    continue
                name, _, rest = line.partition(":")
                name = name.strip()
                if not name:
                    print(f"⚠️  Skipping line {lineno} (empty name).")
                    continue
                scores: list[float] = []
                if rest.strip():
                    try:
                        scores = [float(x) for x in rest.split(",") if x.strip()]
                    except ValueError:
                        print(f"⚠️  Skipping line {lineno} (bad score list).")
                        continue
                students[name] = scores
        print(f"📂 Loaded {len(students)} student(s) from '{path}'.")
    except FileNotFoundError:
        print(f"ℹ️  No file at '{path}' — starting with empty data.")
    except OSError as e:
        print(f"⚠️  Could not read '{path}': {e}")
    return students
# ═════════════════════════════════════════════════════════════
# SGM-9 — menu loop (match/case)
# ═════════════════════════════════════════════════════════════
MENU = """
────────── 📚 Student Grade Manager ──────────
 1) Add student
 2) Add score
 3) Show average
 4) Show top student
 5) Show report
 6) Save to file
 7) Load from file
 8) Exit
──────────────────────────────────────────────
"""


def _prompt(text: str) -> str:
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Bye.")
        raise SystemExit(0)


def main() -> None:
    students: dict[str, list[float]] = {}
    print("Welcome! Starting with empty data.")

    while True:
        print(MENU)
        choice = _prompt("Choose an option (1–8): ").strip()

        match choice:
            case "1":
                add_student(students, _prompt("Student name: "))
            case "2":
                name = _prompt("Student name: ")
                raw = _prompt("Score (0–100): ").strip()
                try:
                    score = float(raw)
                except ValueError:
                    print(f"⚠️  '{raw}' is not a number.")
                    continue
                add_score(students, name, score)
            case "3":
                name = _prompt("Student name: ")
                avg = average(students, name)
                if avg is None:
                    print(f"⚠️  No average for '{name.strip()}'.")
                else:
                    print(f"📊 Average for '{name.strip()}': {avg:.2f}")
            case "4":
                top = top_student(students)
                if top is None:
                    print("ℹ️  No student with scores yet.")
                else:
                    print(f"🏆 Top student: {top} ({average(students, top):.2f})")
            case "5":
                show_report(students)
            case "6":
                path = _prompt(f"File path [{DEFAULT_PATH}]: ").strip() or DEFAULT_PATH
                save_to_file(students, path)
            case "7":
                path = _prompt(f"File path [{DEFAULT_PATH}]: ").strip() or DEFAULT_PATH
                students = load_from_file(path)
            case "8":
                print("👋 Bye.")
                break
            case _:
                print("⚠️  Invalid choice. Pick 1–8.")



if __name__ == "__main__" :


   main()
