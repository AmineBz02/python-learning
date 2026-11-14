def add_student(students: dict, name: str) -> None:
   if name.strip() == "":
      print("Error: Student name cannot be empty.")
      return
   if name in students:
      print(f"Error: Student '{name}' already exists.")
      return
   students[name] = []



def main()-> None:
   return

if __name__ == "__main__" :


   main()
