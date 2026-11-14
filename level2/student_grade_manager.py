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

def main()-> None:
   return

if __name__ == "__main__" :


   main()
