def guessing_game():
    import time
    import random
    import json
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

    def get_guess(min_num, max_num):
        while True:
            try:
                guess = int(input(f"Your guess ({min_num}-{max_num})? "))
                if guess < min_num or guess > max_num:
                    print(f"Guess must be between {min_num} and {max_num}!")
                    continue
                return guess  
            except ValueError:
                print("Invalid! Numbers only.")

    try:
        with open("guessing_scores.txt", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = {
            "higher_lower": [],
            "warmer_colder": []
        }
    score = 0
    difficulty = 0
    difficulty_names = {
        1: "Very Easy",
        2: "Easy",
        3: "Medium",
        4: "Hard",
        5: "Insane"
    }
    if scores["higher_lower"]:
        high_score = min(player["score"] for player in scores["higher_lower"])
    else:
        high_score = None
    print("Welcome to the...")
    time.sleep(1)
    print("*drumroll*")
    time.sleep(2)
    print("The Guessing Game!!!")
    time.sleep(1.5)
    print("Where we give u hints and you Guess away!!!")
    time.sleep(2)

    while True:
        try:
            gmode = int(input("Pick a game mode: Higher/Lower (1) or Warmer/Colder (2): (type 3 to exit ) "))
            if gmode in (1, 2):
                break
            elif gmode == 3:
                break
            else:
                print("Pick 1 or 2 only!")
        except ValueError:
            print("Numbers only!")

    if gmode == 1:
        print("Classic mode, enjoy!")
        view_scores = input("Do you wish to see previous scores? ").strip().lower()

        if view_scores == "yes":
            if not scores.get("higher_lower"):
                print("No scores saved yet.")
            else:
                for i, player in enumerate(
                    sorted(scores["higher_lower"], key=lambda x: x["score"]),
                    start=1
                ):
                    diff = player.get("difficulty")
                    diff_name = difficulty_names.get(diff, "Unknown")
                    print(f"{i}. {player['name']} - {player['score']} guesses - {diff_name}")
        while True:
            min_num, max_num = get_range()
            if max_num - min_num <= 50:
                difficulty = 1
            elif max_num - min_num <= 100:
                difficulty = 2
            elif max_num - min_num <= 150:
                difficulty = 3
            elif max_num - min_num <= 200:
                difficulty = 4
            elif max_num - min_num > 200:
                difficulty = 5
            number = random.randint(min_num, max_num)

            guess = get_guess(min_num, max_num)
            score += 1
            if guess > number:
                print("Lower!")
            elif guess < number:
                print("Higher!")
            else:
                print("Wow, you guessed it!")
                if high_score is None or score < high_score:
                    high_score = score
                    print("NEW HIGH SCORE!")
                if high_score is not None:
                    print(f"Your score: {score}")
                    print(f"Best score ever: {high_score}")
                else:
                    print(f"Your score: {score}")
                save = input("do you want to save your score? ").strip().lower()
                if save == "yes":
                    name = input("Enter your name: ")

                    scores["higher_lower"].append({
                        "name": name,
                        "score": score,
                        "difficulty": difficulty
                    })

                    with open("guessing_scores.txt", "w") as f:
                        json.dump(scores, f, indent=4)

                    print("Score saved!")
                choice = input("Play again? (yes/no) ")
                if choice.lower() == "yes":
                    number = random.randint(min_num, max_num)
                    score = 0
                    continue
                else:
                    print("Aww, fine, have a good day!")
                    break
if __name__ == "__main__":
    guessing_game()
