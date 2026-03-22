from todo_list import todo_list
from guessing_game import guessing_game
from password_gen import pword_gen
from words_password_gen import pword_gen_words
from calculator import calculator
import time
import os
import random
import winsound
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
RESET = "\033[0m"

colors = [RED, GREEN, YELLOW, BLUE, CYAN, MAGENTA]
def clear():
    os.system("cls" if os.name == "nt" else "clear")
clear()
def main_menu():
    while True:
        title_name = "NABIL'S"
        for char in title_name:
            winsound.Beep(random.randint(200,1000),200)
            print(char, end=" ", flush=True)
            time.sleep(0.25)
        print()
        title = "PYTHON PROJECTS"
        winsound.Beep(random.randint(200,1000),200)
        for char in title:
            print(random.choice(colors), char, end="", flush=True)
            time.sleep(0.25)
        print()
        winsound.MessageBeep()
        print(RESET, "\n=== MAIN MENU", "="*26)
        print(f"{GREEN}1. To-Do List{RESET}")
        print(f"{MAGENTA}2. Guess Game{RESET}")
        print(f"{YELLOW}3. Password Generator(random){RESET}")
        print(f"{BLUE}4. Password Generator(with words){RESET}")
        print(f"{CYAN}5. Calculator{RESET}")
        print(f"{RED}6. Quit{RESET}")
        print("="*40)
        choice = input("Choose an option: ").strip()
        freq = 37
        if choice == "1":
            duration = 5
            freq = 700
        elif choice == "2":
            duration = 8
            freq = 500
        elif choice == "3":
            duration = 2
            freq = 400
        elif choice == "4":
            duration = 3
            freq = 150
        elif choice == "5":
            duration = 4
            freq = 250
        elif choice == "6":
            duration = 1
            freq = 100
        winsound.Beep(freq,250)
        end_time = time.time() + duration
        while time.time() < end_time:
            for dots in range(4):  # 0,1,2,3 dots
                print("\rLoading" + "." * dots + "   ", end="", flush=True)
                time.sleep(0.4)    
        print("\rLoading complete!   ")
        winsound.MessageBeep() 
        print("="*40)
        time.sleep(1)
        clear()
        if choice == "1":
            todo_list()
            clear()
        elif choice == "2":
            guessing_game()
            clear()
        elif choice == "3":
            pword_gen()
            time.sleep(2)
        elif choice == "4":
            pword_gen_words()
            time.sleep(2)
        elif choice == "5":
            calculator()
            time.sleep(2)
            clear()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
main_menu()