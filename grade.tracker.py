def add_grade(name, grade):
    with open("grades.txt", "a") as file:
        file.write(name + ":" + str(grade) + "\n")
    print(f"{name} added successfully!")

def view_grades():
    try:
        with open("grades.txt", "r") as file:
            lines = file.readlines()
        
        if len(lines) == 0:
            print("No grades saved yet!")
            return
        
        print("\n--- Grade Report ---")
        total = 0
        for line in lines:
            parts = line.strip().split(":")
            name = parts[0]
            grade = float(parts[1])
            total += grade
            print(f"{name}: {grade}")
        
        average = total / len(lines)
        print(f"Class average: {average:.1f}")
        print("--------------------\n")
    
    except FileNotFoundError:
        print("No grades file found! Add a student first.")

while True:
    print("\n1. Add student")
    print("2. View grades")
    print("3. Quit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        name = input("Student name: ")
        grade = float(input("Grade: "))
        add_grade(name, grade)
    elif choice == "2":
        view_grades()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option!")