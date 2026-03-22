def todo_list():
    import json
    import os
    def clear():
        os.system("cls" if os.name == "nt" else "clear")
    try:
        with open("tasks.txt", "r") as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    while True:
        try:
            action = input("Do you want to view, add, remove, or check off tasks? (or 'no' to quit) ").lower().strip()
            if action == "no":
                break

            if len(tasks) == 0 and (action in ["view", "remove", "check off"]):
                print("You don't have any tasks yet!")
                continue
        
            if action == "view":
                print("Your tasks:")
                for i, t in enumerate(tasks, start=1):
                    checkbox = "[X]" if t["done"] else "[ ]"
                    print(f"{i}. {checkbox} {t['task']}")

            elif action == "add":
                task_name = input("What is the task you wish to add? ").strip()
                tasks.append({"task": task_name, "done": False})
                print(f"'{task_name}' added!")
                clear()

            elif action == "remove":
                for i, t in enumerate(tasks, start=1):
                    checkbox = "[X]" if t["done"] else "[ ]"
                    print(f"{i}. {checkbox} {t['task']}")
                to_remove = int(input("Which task number do you want to remove? "))
                if 1 <= to_remove <= len(tasks):
                    removed = tasks.pop(to_remove - 1)
                    print(f"'{removed['task']}' removed!")
                    clear()
                else:
                    print("Invalid task number.")

            elif action == "check off":
                for i, t in enumerate(tasks, start=1):
                    checkbox = "[X]" if t["done"] else "[ ]"
                    print(f"{i}. {checkbox} {t['task']}")

                to_check = int(input("Which task number do you want to toggle? "))

                if 1 <= to_check <= len(tasks):
                    task = tasks[to_check - 1]

                    if task["done"]:  
                        un_check = input(f"'{task['task']}' is already checked. Uncheck it? (yes/no) ").strip().lower()

                        if un_check == "yes":
                            task["done"] = False
                            print(f"'{task['task']}' is now unchecked!")
                        else:
                            print("Nothing changed.")

                    else:  
                        task["done"] = True
                        print(f"'{task['task']}' checked off!")
            
                else:
                    print("Invalid task number.")

            else:
                print("Invalid action. Choose view, add, remove, or check off.")
            with open("tasks.txt", "w") as f:
                json.dump(tasks, f)
        except(ValueError):
            print("Inavlid input.")
if __name__ == "__main__":
    todo_list()
        
