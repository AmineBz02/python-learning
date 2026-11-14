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


def main()-> None:
   return

if __name__ == "__main__" :


   main()
