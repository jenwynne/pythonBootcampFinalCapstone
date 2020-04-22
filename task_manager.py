# datetime is imported to ensure that dates entered are uniform and comparable:
import datetime

# This programme allows users to login, register new users, add and edit tasks,
# view all tasks, view only their tasks and view information about all tasks
# and users.

# FUNCTION1 *********************************************
# The first function provides the user with all the options avialable to them
# Depending on which option is selected a specific function is called,
# followed by an opportunity to recall the options function

def options():

    # the admin user will be given additional options for reporting purposes:
    if logged_in == "admin":
        choice = input("Please select one of the following options:\n\t\
                        r - register user\n\t\
                        a - add task\n\t\
                        va - view all tasks\n\t\
                        vm - view my tasks\n\t\
                        gr - generate reports\n\t\
                        ds - display statistics\n\t\
                        e - exit")

    else:
        choice = input("Please select one of the following options:\n\t\
                        r - register user\n\t\
                        a - add task\n\t\
                        va - view all tasks\n\t\
                        vm - view my tasks\n\t\
                        e - exit")

    # REGISTERING A USER
    if choice == "r":
        reg_user(logged_in)
        
        # At the end of each option, the user is offered another round
        options2()
  
    # ADDING A TASK
    if choice == "a":
        add_task()

        options2()
    
    # VIEW ALL TASKS
    if choice == "va":
        view_all()

        options2()


    # VIEW MY TASKS
    if choice == "vm":
        view_mine()

        options2()
            
    # GENERATE REPORTS
    if choice == "gr":
        gen_reports()

        options2()


    # VIEW USER STATISTICS(admin only)
    if choice == "ds":
        gen_reports()

        print("User and task information:")

        users = open("user_overview.txt", "r")
        user_info = users.read()
        total_users = user_info.count("User:")
        print("Total number of users currently registered:\t{}".format(total_users))
        users.close()

        tasks = open("task_overview.txt", "r")
        task_info = tasks.read()
        print("Total number of tasks currently listed:\t\t{}".format(task_info.split(" ")[6].strip("\nTotal")))
        tasks.close()

        options2()

    # EXIT
    if choice == "e":
        print("Thank you, good bye")
        quit()

# FUNCTION 2 *********************************************
# This function checks if the user still has more work to do, if so it offers
# the options list again:

def options2():
    choice2 = input("Would you like to select another option? y/n")
    if choice2 == "y":
        options()
    if choice2 == "n":
        print("Thank you, good bye")
    

# FUNCTION 3 *********************************************
# This function checks if the user is authorised to register a user, if so the
# user is asked to input a username and 2 matching passwords.

def reg_user(logged_in):
    users = open("user.txt", "r+")
    user_info = users.readlines()

    # If statement ensures that only admin user will be allowed to register
    # new users
    if logged_in == "admin":
    
        print("Registering a new user:")
        username = input("Please type the username: ")

        # loop through all usernames already listed:
        name_taken = False

        for line in user_info:
            
            if line.split(" ")[0].strip(",") == username:
                name_taken = True

            if line.split(" ")[0].strip(",") != username:
                name_taken == False
                continue
            
        # while condition refuses entry of a duplicated username:
        while name_taken == True:
            print("This user already exists")
            username = input("Please type the username: ")

            name_taken = False

            for line in user_info:

                if line.split(" ")[0].strip(",") == username:
                    name_taken = True

                if line.split(" ")[0].strip(",") != username:
                    name_taken == False
                    continue
                
        # if the username is not a duplicate, the programme requests a password:
        if name_taken == False:
            password = input("Please type in the password: ")
            password2 = input("Please confirm your password: ")

            # Checks that passwords match:
            while password != password2:
                print("Your passwords do no match, please try again: ")
                password = input("Please type in the password: ")
                password2 = input("Please confirm your password: ")
            print("Thank you, your passwords match.")   
            
            # Writes new username and password to user doc
            users.write("\n" + username +", ")
            users.write(password)

    # If user is not admin, execute print statement
    else:
        print("Sorry, only the admin user is allowed to register new users.")

        users.close()
        
# FUNCTION 4 *********************************************
# This function checks that the date has been entered in the correct format
# This ensures that the dates can be saved in a meaningful way and compared

def check_date(task_due):
    
    if len(task_due) > 10:
            print("Please make sure you enter YYYY-MM-DD, eg: 2020-03-15")
            task_due = input("Please enter the due date for this task")
            return check_date(task_due)
    else:
        a = task_due.split("-")[0]
        b = task_due.split("-")[1]
        c = task_due.split("-")[2]
       
        date_correct = False

        while date_correct == False:

            if (2019 < int(a) < 2040) and (0 < int(b) < 13) and (0 < int(c) < 32):
                date_correct = True
                correct_date = task_due
                return correct_date
                   
            else:
                date_correct = False
                print("Please make sure you enter YYYY-MM-DD, eg: 2020-03-15")
                task_due = input("Please enter the due date for this task")
                return check_date(task_due)


# FUNCTION 5 *********************************************
# This function allows the user to add a task.

def add_task():
    
    print("Adding a task:")

    # First step is assigning task to a user, this checks that user entered
    # is a registered user
    # Is the user is not registered, it prompts for another entry
    # If the user is registered, it moves on to the next question

    users = open("user.txt", "r")
    user_info = users.readlines()

    user_for_task = False
    
    while user_for_task == False:
        task_user = input("What is the username of the person you are assigning this task to?")
        
        for line in user_info:
            if line.split(" ")[0].strip(",") == task_user:
                user_for_task = True 
            else:
                user_for_task = False
                continue
            break

        if user_for_task:
            task_title = input("What is the title of this task?")
            
        if not user_for_task:
            print("Please make sure you enter a user that is registered on the system.")

    users.close()

    tasks = open("tasks.txt", "a")

    # Other questions regarding task:
    task_des = input("Please describe this task")

    task_due = input("What is the due date of this task? (YYYY-MM-DD)")
    correct_date = check_date(task_due)
    
    task_assn_date = datetime.date.today()
    completed = "No"

    # Task info written to task doc
    tasks.write(task_user +";")
    tasks.write(task_title +";")
    tasks.write(task_des +";")
    tasks.write(str(task_assn_date) +";")
    tasks.write(correct_date +";")
    tasks.write(completed + "\n")

    tasks.close()

# FUNCTION 6 *********************************************
# This function allows the user to view all the tasks listed

def view_all():
    tasks = open("tasks.txt", "r")

    print("All Tasks:")

    # Each line in tasks is its own task, so for every task print details
    # of task, this also allows the task to be identified by its index no.:
    task_list = []
    for line in tasks:
        task_list.append(line)

    for i in task_list:
        print("Task number:\t\t{}".format(task_list.index(i)+1))
        print("Task assigned to:\t{}".format(i.split(";")[0]))
        print("Title:\t\t\t{}".format(i.split(";")[1]))
        print("Task Description:\t{}".format(i.split(";")[2]))
        print("Task assigned on:\t{}".format(i.split(";")[3]))
        print("Task due on:\t\t{}".format(i.split(";")[4]))
        print("Task completed:\t\t{}".format(i.split(";")[5]))

    tasks.close()

# FUNCTION 7 *********************************************
# This function allows the user to view the tasks assigned to them and select
# a task to edit

def view_mine():
    tasks = open("tasks.txt", "r")

    # Counter to check number of tasks for this user:
    number_of_tasks = 0

    print("All My Tasks:")

    # Each line in tasks is its own task, so for every task print details
    # of task, this also allows the task to be identified by its index no.:
    task_list = []
    for line in tasks:
        task_list.append(line)

    for i in task_list:
        if i.split(";")[0] == logged_in:
            print("Task number:\t\t{}".format(task_list.index(i)+1))
            print("Task assigned to:\t{}".format(i.split(";")[0]))
            print("Title:\t\t\t{}".format(i.split(";")[1]))
            print("Task Description:\t{}".format(i.split(";")[2]))
            print("Task assigned on:\t{}".format(i.split(";")[3]))
            print("Task due on:\t\t{}".format(i.split(";")[4]))
            print("Task completed:\t\t{}".format(i.split(";")[5]))
            number_of_tasks += 1

    # if there are no tasks for this user:
    if number_of_tasks == 0:
        print("You have no tasks currently assigned")

    # if there are tasks for this user:
    if number_of_tasks >= 1:

        choice_to_edit = input("If you would like to edit or complete a task, please enter the task number, alternatively enter -1 for the main menu:")

        # If the user does not wish to select a task, this will return to options:
        if choice_to_edit == "-1":
            options()

        # If the user enters a task number that does not have a task assigned
        # to it, an error message is printed:
        elif int(choice_to_edit) > len(task_list):
            print("Sorry that is not a valid entry")
            options()

        else:
            edit_task(choice_to_edit)
                     
    tasks.close()

# FUNCTION 8 *********************************************
# This function allows the user to edit a task

def edit_task(choice_to_edit):

    tasks = open("tasks.txt", "r")

    # Each line in tasks is its own task, so for every task print details
    # of task, this also allows the task to be identified by its index no.:
    task_list = []
    for line in tasks:
        task_list.append(line)

    for i in task_list:
        if int(choice_to_edit) == task_list.index(i)+1:
            print("Task number:\t\t{}".format(task_list.index(i)+1))
            print("Task assigned to:\t{}".format(i.split(";")[0]))
            print("Title:\t\t\t{}".format(i.split(";")[1]))
            print("Task Description:\t{}".format(i.split(";")[2]))
            print("Task assigned on:\t{}".format(i.split(";")[3]))
            print("Task due on:\t\t{}".format(i.split(";")[4]))
            print("Task completed:\t\t{}".format(i.split(";")[5]))

            # for the purposes of re-writing the task, variables are assigned
            # to each piece if info in each task:
            name = i.split(";")[0]
            title = i.split(";")[1]
            description = i.split(";")[2]
            date_assn = i.split(";")[3]
            due_date = i.split(";")[4]
            completed = i.split(";")[5]

    tasks.close()

    # The user can choose to complete or edit the task they have selected:
    edit_choice = input("Please select one of the following options:\n\t\
                        c - complete task\n\t\
                        e - edit task")
    # If the user selects c, programme checks that task is currently not yet
    # completed:
    if edit_choice == "c":
        tasks = open("tasks.txt", "r").readlines()
        if (tasks[int(choice_to_edit) - 1].split(";")[5].strip("\n")) == "Yes":
            print("This task has already been completed")

        # If the task is still incomplete, the task line is rewritten to the file
        # changing only the completed status of the task:
        else:
            tasks[int(choice_to_edit) - 1] = ((name +";") + (title +";") + (description +";") + (date_assn +";") + (due_date +";") + ("Yes\n"))
            output = open("tasks.txt", "w")
            output.writelines(tasks)
            print("Task number {} has been marked as complete".format(int(choice_to_edit)))
            output.close()
            
    # If user selects e, programme checks that tasks is currently not yet
    # complete, if so, user can choose to edit user or due date:
    if edit_choice == "e":
        tasks = open("tasks.txt", "r").readlines()
        if (tasks[int(choice_to_edit) - 1].split(";")[5].strip("\n")) == "Yes":
            print("This task has already been completed and so cannot be edited")

        else:
            edit_choice2 = input("Please select one of the following options:\n\t\
                        u - change user assingned to task\n\t\
                        d - change due date")
        
            # if the user selects u, the programme will check that the new user
            # is a registered user:
            if edit_choice2 == "u":
                users = open("user.txt", "r")
                user_info = users.readlines()
                new_user_for_task = False
                while new_user_for_task == False:
                    task_user = input("Please enter the name of the new user for the task:")
                    for line in user_info:
                        if line.split(" ")[0].strip(",") == task_user:
                            new_user_for_task = True
                        else:
                            new_user_for_task = False
                            continue
                        break
                    if new_user_for_task:
                        print("Changing user assigned to this task...")
                        break
                    if not new_user_for_task:
                        print("Please make sure you enter a user that is registered on the system.")
                users.close()
                
                # Once the user has entered a new valid username, the line is
                # rewritten changing only the user assigned:
                tasks = open("tasks.txt", "r").readlines()
                tasks[int(choice_to_edit) - 1] = ((task_user +";") + (title +";") + (description +";") + (date_assn +";") + (due_date +";") + (completed))
                output = open("tasks.txt", "w")
                output.writelines(tasks)
                print("The user for this task has been change to {}".format(task_user))
                output.close()

            # if the users selects d, the programme requests the new date and
            # checks that the date is in the correct format using the
            # check date function:
            if edit_choice2 == "d":
                task_due = input("What is the new due date for this task? (YYYY-MM-DD)")
                correct_date = check_date(task_due)

            # once a valid date is entered, the line is rewritten changing
            # only the due date:
                tasks = open("tasks.txt", "r").readlines()
                tasks[int(choice_to_edit) - 1] = ((name +";") + (title +";") + (description +";") + (date_assn +";") + (str(correct_date) +";") + (completed))
                output = open("tasks.txt", "w")
                output.writelines(tasks)
                print("The due date for this task has been change to {}".format(correct_date))
                output.close()

# FUNCTION 9 *********************************************
# This function generates reports that are written to 2 text docs

def gen_reports():
    
    # TASK REPORT
    # By looping through all the tasks in the task file, the programme
    # identifies the total number of: tasks, completed tasks, uncompleted
    # tasks & uncompleted overdue tasks:
    tasks = open("tasks.txt", "r")
    all_tasks = tasks.readlines()
    
    total_number_of_tasks = 0
    for line in all_tasks:
        total_number_of_tasks += 1

    total_completed_tasks = 0
    for line in all_tasks:
        if line.split(";")[5].strip("\n") == "Yes":
            total_completed_tasks += 1
            
    total_uncompleted_tasks = 0
    for line in all_tasks:
        if line.split(";")[5].strip("\n") == "No":
            total_uncompleted_tasks += 1
            
    uncom_overdue = 0
    today = str(datetime.date.today())
    today_final = datetime.datetime.strptime(today, "%Y-%m-%d")
    
    for line in all_tasks:
        if line.split(";")[5].strip("\n") == "No":
            due_date = datetime.datetime.strptime(line.split(";")[4], "%Y-%m-%d")
 
            if due_date < today_final:
                uncom_overdue += 1
                

    # percentages are calculated using variables identified from task file:
    perc_incomplete = (total_uncompleted_tasks / total_number_of_tasks) * 100
    perc_incomp_overdue = (uncom_overdue/total_number_of_tasks) * 100

    # tasks stats are written to task overview doc:
    task_report = open("task_overview.txt","w+")
    task_report.write("Task Report\n\n")
    task_report.write("Total number of tasks generated:\t\t {}\n".format(total_number_of_tasks))
    task_report.write("Total number of completed tasks:\t\t {}\n".format(total_completed_tasks))
    task_report.write("Total number of uncompleted tasks:\t\t {}\n".format(total_uncompleted_tasks))
    task_report.write("Total number of uncompleted overdue tasks:\t {}\n".format(uncom_overdue))
    task_report.write("Percentage of tasks that are incomplete:\t {}%\n".format(int(perc_incomplete)))
    task_report.write("Percentage of tasks that are overdue:\t\t {}%\n".format(int(perc_incomp_overdue)))

    task_report.close()
    tasks.close()

    # USER REPORT:

    users = open("user.txt", "r")
    all_users = users.readlines()

    tasks = open("tasks.txt", "r")
    all_tasks = tasks.readlines()

    # Total number of users is identified:
    total_number_of_users = 0
    for line in all_users:
        total_number_of_users += 1

    user_report = open("user_overview.txt","w+")
    user_report.write("Number of tasks per user\n\n")  

    # for loop looks at each user listed and then nested loop checks which
    # tasks are assigend to this user:
    for user in all_users:
        this_user = user.split(",")[0]

        num_tasks_for_user = 0
        total_comp = 0
        total_not_comp = 0
        total_not_comp_overdue = 0

        today = str(datetime.date.today())
        today_final = datetime.datetime.strptime(today, "%Y-%m-%d")

        for task in all_tasks:
            due_date = datetime.datetime.strptime(task.split(";")[4], "%Y-%m-%d")
            
            if task.split(";")[0] == this_user:
                num_tasks_for_user += 1
    
            if (task.split(";")[0] == this_user) and (task.split(";")[5].strip("\n") == "No") and (due_date < today_final):
                    total_not_comp_overdue += 1
        
            if (task.split(";")[0] == this_user) and (task.split(";")[5].strip("\n") == "Yes"):
                    total_comp += 1
       
            if (task.split(";")[0] == this_user) and (task.split(";")[5].strip("\n") == "No"):
                    total_not_comp += 1

        # If no tasks are assigned to this user, user is listed as not having
        # any tasks:
        if num_tasks_for_user == 0:
            user_report.write("User:\t\t\t\t\t\t\t{}\n".format(this_user))
            user_report.write("Total tasks:\t\t\t\t\t\t{}\n".format(num_tasks_for_user))
            user_report.write("No further data is available as this user has no tasks.\n\n")

        # If the user has at least 1 task, all data for users tasks is written
        # to file:
        if num_tasks_for_user > 0:
            
            perc_of_all_tasks = int((num_tasks_for_user / total_number_of_tasks) * 100)
            perc_comp = int((total_comp / num_tasks_for_user) * 100)
            perc_to_comp = int((total_not_comp / num_tasks_for_user) * 100)
            perc_to_comp_overdue = int((total_not_comp_overdue / num_tasks_for_user) * 100)
            
            user_report.write("User:\t\t\t\t\t\t\t{}\n".format(this_user))
            user_report.write("Total tasks:\t\t\t\t\t\t{}\n".format(num_tasks_for_user))
            user_report.write("Users percentage of all tasks:\t\t\t\t{}%\n".format(perc_of_all_tasks))
            user_report.write("Percentage user tasks completed:\t\t\t{}%\n".format(perc_comp))
            user_report.write("Percentage user tasks to be completed:\t\t\t{}%\n".format(perc_to_comp))
            user_report.write("Percentage user tasks to be completed that are overdue:\t{}%\n\n".format(perc_to_comp_overdue))

    user_report.close()
    users.close()
    tasks.close()
                                  
#********************************************* END OF FUNCTIONS ************************************************************************

# LOGIN ************************************

# Open the user file and read:
users = open("user.txt", "r")
user_info = users.readlines()

# Programme assumes that user has not entered a valid username or password: 
access1 = False
access2 = False

# While loop - as long as username is incorrect - prompts user for username
# For loop checks each line of user info
# If username is correct, move onto password
# While password is incorrect, prompt user for password 
while access1 == False:
    username = input("Username: ")
    
    for line in user_info:

        if line.split(" ")[0].strip(",") == username:
            access1 = True

            while access2 == False:
                password = input("Password: ")

                if line.split(" ")[1].strip("\n") == password:
                    access2 = True
                    break
   
                else:
                    access2 = False
                    print("Your password is incorrect, please try again")
                    continue         
        else:
            access1 = False
            continue
        break

    if (not access1) and (not access2):
        print("Your username is not registered, please try again")

    if (access1) and (not access2):
        print("Your password is incorrect, please try again")

    if (access1) and (access2):
        print("You have successfully logged in.")
        break
    
users.close()

logged_in = username

options()
