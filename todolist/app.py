tasks = []

#add tasks and deadlines
def add_task():
    taskName = input("enter your task here: ")
    deadline = input("add a deadline here: ")
    task = {
        "taskName" : taskName,
        "deadline" : deadline,
        "done" : False,
        }
    tasks.append(task)
    print("Task Added!")

# view tasks    
def view_task():
    if len(tasks) == 0:
        print("no task added yet")
        return
    for i in range(len(tasks)):
        if tasks[i]["done"] == True:
            status = ("Task completed")
        else:
            status = ("pending")
        print(str(i + 1) + ". " + tasks[i]["taskName"] + " Due: " + tasks[i]["deadline"] + " : " + status)

# mark as done
def mark_done():
    view_task()
    while True:
        user_input = (input("enter number of the task ya wanna mark as done here: "))
        if user_input.isdigit() == True:
           num = int(user_input)
           tasks[num-1]["done"] = True
           print("Marked as done!🥂🎊🪅")
           break
        else:
           print("inavlid number!🥴")
    

#delete a task
def del_task():
    view_task()
    while True:
        user_Input = (input("enter number of the task ya would like to delete: "))
        if user_Input.isdigit() == True:
           num = int(user_Input)
           removed = tasks.pop(num-1)
           print("task deleted!💃", removed)
           break
        else:
           print("Invalid Number!🥴")

while True:
    print("\n1. Add Task\n2. View Task\n3. Mark task\n4. Delete Task\n5. Exit")
    choice = (input("choose: "))
    if choice == "1":
        add_task()
    elif choice == "2":
        view_task()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        del_task()
    elif choice == "5":
        break