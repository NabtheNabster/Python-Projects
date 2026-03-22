def pword_gen_words():
    import random
    chars = {
        "symbols": ["!", "£", "$", "%", "^", "&", "*", "(", ")"],
        "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "numbers": list("0123456789")
    }
    with open("words.txt", "r") as f:
        words = [line.strip() for line in f.readlines()]
    while True:
        try:
            length = int(input("How many char+word pairs do you want? "))
            password_parts = []
            for _ in range(length):
                char = random.choice(chars["letters"] + chars["numbers"] + chars["symbols"])
                if char.isalpha() and random.random() < 0.5:
                    char = char.lower()
                password_parts.append(char)
                
                word = random.choice(words)
                password_parts.append(word)
            char = random.choice(chars["letters"] + chars["numbers"] + chars["symbols"])
            if char.isalpha() and random.random() < 0.5:
                char = char.lower()
            password_parts.append(char)
            password = "".join(password_parts)
            print(password)
            choice = input("Would you like to generate another password?(yes/no) ")
            if choice != "yes":
                print("Have a good day then!")
                break
        except(ValueError):
            print("Invalid input")
            continue
if __name__ == "__main__":
    pword_gen_words()