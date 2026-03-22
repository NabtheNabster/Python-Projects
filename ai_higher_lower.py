import random
import os
def clear():
    os.system("cls" if os.name == "nt" else "clear")
clear()
def get_range():
    while True:
        try:
            min_num = int(input("What is the minimum for the range? "))
            max_num = int(input("What is the max for the range? "))
            if max_num > 1000:
                sure = input("Over 1000 is hard, sure you want to do this? (yes/no) ")
                if sure.lower() != "yes":
                    continue
            if min_num >= max_num:
                print("Minimum must be less than maximum!")
                continue
            return min_num, max_num
        except ValueError:
            print("Invalid input! Numbers only.")

def ai_binary_guess(low, high):
    return (low + high) // 2
again = True
while again:
    min_num, max_num = get_range()
    number = random.randint(min_num, max_num)
    score = 0
    low = min_num
    high = max_num

    while True:
        guess = ai_binary_guess(low, high)
        print(f"AI guesses: {guess}")
        score += 1
        if guess > number:
            print("Lower!")
            high = guess - 1
        elif guess < number:
            print("Higher!")
            low = guess + 1
        else:
            print(f"Wow, AI guessed it! The number was {number}")
            print(f"Score: {score}")
            break
    retry = input("Go again? ")
    if retry.lower() == "y" or retry.lower() == "yes":
        print("Good luck!")
    else:
        again = False