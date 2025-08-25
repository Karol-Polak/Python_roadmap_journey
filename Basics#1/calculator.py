#Basic calculator in python, user operates it by inputs
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
operation = input("Enter the operation (+, -, *, /): ")

if operation == "+":
    print(a + b)
elif operation == "-":
    print(a - b)
elif operation == "*":
    print(a * b)
elif operation == "/":
    if b != 0:
        print(a / b)
    else:
        print("Dividing by zero is not possible")
