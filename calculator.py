def calculator():
    print("Welcome to the ultimate calculator!")
    retry = True
    while retry == True:
        try:
            num_ops = int(input("How many operations will you use? "))

            numbers = []
            operators = []

            for i in range(num_ops + 1):  
                num = float(input(f"Enter number {i+1}: "))
                numbers.append(num)
        
            for i in range(num_ops):  
                op = input(f"Enter operator {i+1} +(1), -(2), *(3), /(4): ")
                if op == "1":
                    op = "+"
                elif op == "2":
                    op = "-"
                elif op == "3":
                    op = "*"
                elif op == "4":
                    op = "/"
                if op not in "+-*/":
                    raise ValueError
                operators.append(op)

            expression = ""
            for i in range(num_ops):
                expression += str(numbers[i]) + " " + operators[i] + " "
            expression += str(numbers[-1])  

            print("\nYour problem:")
            print(expression)

            result = eval(expression)
            print("\nResult:")
            print(result)
        except ValueError:
            print("Invalid input retry!")
            continue
        choice = input("Do you want to do another calculation? (yes/no): ")
        if choice.lower() != "yes":
            retry = False
if __name__ == "__main__":
    calculator()