def pword_gen():
    import random
    chars = {
        "symbols":["!","£","$","%","^","&","*","(",")"],
        "letters":["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
        "numbers":["0","1","2","3","4","5","6","7","8","9"]
    }
    all_chars = chars["symbols"]+chars["letters"]+chars["numbers"]
    while True:
        try:
            length = int(input("How long should your password be? "))
            password_chars = []

            for _ in range(length):
                char = random.choice(all_chars)
                if char.isalpha() and random.random() < 0.5:
                    char = char.lower()
                password_chars.append(char)

            password = "".join(password_chars)
            print(password)
            choice = input("Would you like to generate another password?(yes/no) ")
            if choice != "yes":
                print("Have a good day then!")
                break
        except(ValueError):
            print("Invalid input")
            continue
if __name__ == "__main__":
    pword_gen()