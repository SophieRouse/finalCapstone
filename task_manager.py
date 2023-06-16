# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# tasks.txt is read and split at each new line
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# A list is used for the tasks.
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    # Each task is added to the task list
    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert user data to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password


# logged_in is false to make a user sign in
logged_in = False
while not logged_in:

# User is asked to input their username and password
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    # - Error message given if username is not in the txt file
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    # - The user is given an error message if they do not input the correct password
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    # - If details are correct, user is logged in and shown a successful message
    else:
        print("Login Successful!")
        logged_in = True

# reg_user function is used to create new users
def reg_user():
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        # - Check if the new username already exists
        if new_username in username_password.keys():
            print("Username already exists in database, please enter another username.")
        else:
            break
    # - Request input of a new password
    new_password = input("New Password: ")
    # - Request input of password confirmation
    confirm_password = input("Confirm Password: ")
    # - Check if the new password and confirmed password are the same
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file
        print("New user added")
        username_password[new_username] = new_password
        
        # - user data is added to txt file and a list
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # - Otherwise user is given a message showing error
    else:
        print("Passwords do no match")

# function is used to add tasks to a user
def add_task():
    
    # - user prompted to insert the person the task is assigned to
    task_username = input("Name of person assigned to task: ")
    # - error given if user is not found
    if task_username not in username_password.keys():
        return print("User does not exist. Please enter a valid username")
    # - user prompted to input title of task
    task_title = input("Title of Task: ")
    # - user prompted to input description of task
    task_description = input("Description of Task: ")
    while True:
        try:
            # - user prompted to input date task is due
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        
        # - If user inputs date wrong, they get an error message
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
    # Then get the current date.
    curr_date = date.today()
    # - dictionary used to keep track of task data
    # - false is used to show task is not complete
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # - new tasks are added to tasks.txt file
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# function used to allow user to view all tasks
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# function used to allow user to view all of their tasks
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)
    '''
    my_tasks = {}
    for task_num, t in enumerate(task_list):
        if t['username'] == curr_user:
            my_tasks[str(task_num)] = t
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Task number: \t {task_num}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    # User can edit task by selecting the task by number
    edit_opt = input("Please select a task to edit by entering a task number or enter -1 to go to main menu: ").lower()
    # - user can return to main menu
    if edit_opt == "-1":
        return print("Back to main menu\n")
    # - user can mark a task complete or edit a task
    elif edit_opt in my_tasks.keys():
        complete_or_edit = input("Please enter: \tmc - to mark complete\n\t\tet - to edit task : ").lower()
        # - mc marks the task complete
        if complete_or_edit == "mc":
            task_list[int(edit_opt)]['completed'] = True
        # - et allows user to edit the task only if not completed
        elif complete_or_edit == "et":
            if task_list[int(edit_opt)]['completed']:
                return print("This task has already been completed and cannot be edited.")
            else:
                # - user can assign task to different user or change due date
                name_or_date = input("Please enter: \tun - to change assigned user\n\t\tdd - to change due date : ").lower()
                # - un allows user to reassign the task
                if name_or_date == "un":
                    while True:
                        # - Request input of new assigned user
                        assign_user = input("Who should this task be reassigned to: ")
                        # - Check if the username exists.
                        if assign_user in username_password.keys():
                            task_list[int(edit_opt)]["username"] = assign_user
                            break
                        # - error message given if reassigned user is not found
                        else:
                            print("Username does not exist in database, please enter another username.")
              
                # - dd allow user to change due date
                elif name_or_date == "dd":
                    while True:
                        # - user can input new due date
                        try:
                            new_task_due_date = input("New due date of task (YYYY-MM-DD): ")
                            new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                            break
                        # - error given if date is inputted in an incorrect format
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                    # - new due date is recorded
                    task_list[int(edit_opt)]["due_date"] = new_due_date_time
                # - error message given if incorrect entry
                else:
                    return print("Invalid Option, please try again.")
        
        # - error message given if invalid input
        else:
            return print("Invalid input, please try again.")
        # - tasks written to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        # - acknowledge to user that the task has been updated
        print("Task successfully updated.")
    # - error message given for invalid entry
    else:
        print("Please enter a valid task number.")

# function used to generate user reports
def generate_reports():
    # - len used to give the number of tasks tracked
    tasks_tracked = len(task_list)
    # - incomplete tasks listed
    incomplete_tasks = []
    # - completed tasks listed
    complete_tasks = []
    # - overdue tasks listed
    overdue_tasks = []
    # - for loop used to add users to lists based on task completion
    for t in task_list:
        if t["completed"]:
            complete_tasks.append(t["username"])
        else:
            incomplete_tasks.append(t["username"])
            if t["due_date"] < datetime.today():
                overdue_tasks.append(t["username"])
    # - calculation to show % of the tasks the user has not completed
    percent_incomplete = 100.0 * float(len(incomplete_tasks))/float(tasks_tracked)
    # - calculation to show % of the tasks the user has left overdue
    percent_overdue = 100.0 * float(len(overdue_tasks))/float(tasks_tracked)

    # counts registered users
    registered_users = len(username_password.keys())
    incomplete = {}
    complete = {}
    overdue = {}
    total = {}
    # for loop used to count number of complete, incomplete and overdue tasks per user, adds them to the dictionaries and prints them
    for user in username_password.keys():
        incomplete[user] = incomplete_tasks.count(user)
        complete[user] = complete_tasks.count(user)
        overdue[user] = overdue_tasks.count(user)
        total[user] = incomplete[user]+complete[user]
    # - Outputs written to txt file
    with open("task_overview.txt", "w") as task_overview:
        output_t_overview = f"Total Tasks:\t\t{tasks_tracked}\n"
        output_t_overview += f"Completed Tasks:\t{len(complete_tasks)}\n"
        output_t_overview += f"Incomplete Tasks:\t{len(incomplete_tasks)}\n"
        output_t_overview += f"Overdue Tasks:\t\t{len(overdue_tasks)}\n"
        output_t_overview += f"Percentage of Tasks incomplete:\t{percent_incomplete:.2f}%\n"
        output_t_overview += f"Percentage of Tasks overdue:\t{percent_overdue:.2f}%\n"
        task_overview.write(output_t_overview)

    # - Outputs written to txt file
    with open("user_overview.txt", "w") as user_overview:
        output_u_overview = f"Total Users:\t\t{registered_users}\n"
        output_u_overview += f"Total Tasks:\t\t{tasks_tracked}\n"
        output_u_overview += f"USER\t\tTASKS\t\t%ASSIGNED\t%COMPLETE\t%INCOMPLETE\t%OVERDUE\n"
        for user in username_password.keys():
            output_u_overview += f"{user}:\t\t{total[user]}"
            output_u_overview += f"\t\t{100.0*total[user]/tasks_tracked:.2f}"
            # - If user has not been assigned any tasks, if statement prevents error of dividing by 0
            if total[user] == 0:
                output_u_overview += f"\t\tN/A"
                output_u_overview += f"\t\tN/A"
                output_u_overview += f"\t\tN/A\n"
            # - Outputs % of tasks user has completed, not complete and overdue. Formatting ensures 2 dp
            else:
                output_u_overview += f"\t\t{100.0*complete[user]/total[user]:.2f}"
                output_u_overview += f"\t\t{100.0*incomplete[user]/total[user]:.2f}"
                output_u_overview += f"\t\t{100.0*overdue[user]/total[user]:.2f}\n"
        user_overview.write(output_u_overview)
        

        

    


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    # when user selects r, they can register a new user
    if menu == 'r':
        reg_user()
    
    # when user selects a, they can add a task
    elif menu == 'a':
        add_task()

    # when user selects va, they can view all tasks assigned
    elif menu == 'va':
        view_all()

    # when user selects vm, they can view all taskes assigned to them
    elif menu == 'vm':
        view_mine()
    
    # when user selects gr, a report is generated 
    elif menu == 'gr':
        generate_reports()

    # when user selects ds, if they are an admin they can view user statistics
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        # Prints to terminal
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    # when user selects e, they exit the menu and log out
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # when user inputs an invalid entry, they get an error message
    else:
        print("You have made a wrong choice, Please Try again")