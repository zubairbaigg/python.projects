print("Welcome to the calculator!")
print("Type 'quit' at any time to exit")

while True:
    try:
        num1 = input("Enter first number: ")
        if num1 == "quit":
            print("Goodbye!")
            break

        num1 = float(num1)
        
        num2 = input("Enter second number: ")
        if num2 == "quit":
            print("Goodbye!")
            break

        num2 = float(num2)
        
        operator = input("Enter operation (+, -, *, /): ")
        if operator == "quit":
            print("Goodbye!")
            break

        if operator == "+":
            print("Answer:", num1 + num2)
        elif operator == "-":
            print("Answer:", num1 - num2)
        elif operator == "*":
            print("Answer:", num1 * num2)
        elif operator == "/":
            if num2 == 0:
                print("Error: Can't divide by zero!")
            else:
                print("Answer:", num1 / num2)
        else:
            print("Invalid operator!")

    except ValueError:
        print("Error: Please enter valid numbers only!")

    print("----------------------------")