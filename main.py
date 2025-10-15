# main.py
from manager import Manager

def show_menu():
    print("\n=== ToDoList CLI ===")
    print("1. Create Project")
    print("2. Show All Projects")
    print("3. Add Task to Project")
    print("4. Edit Task Status")
    print("5. Delete Task")
    print("6. Delete Project")
    print("7. Exit")
    return input("Choose option: ")

def main():
    manager = Manager()
    while True:
        choice = show_menu()
        if choice == '1':
            name = input("Enter project name: ").strip()
            manager.add_project(name)
        elif choice == '2':
            manager.show_all_projects()
        elif choice == '3':
            project_name = input("Project name: ").strip()
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()
            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            manager.add_task_to_project(project_name, title, description, deadline)
        elif choice == '4':
            project_name = input("Project name: ").strip()
            task_title = input("Task title to edit: ").strip()
            new_status = input("New status (pending/completed): ").strip()
            manager.update_task_status(project_name, task_title, new_status)
        elif choice == '5':
            project_name = input("Project name: ").strip()
            task_title = input("Task title to delete: ").strip()
            manager.delete_task_from_project(project_name, task_title)
        elif choice == '6':
            project_name = input("Project name to delete: ").strip()
            manager.delete_project(project_name)
        elif choice == '7':
            print("Exiting. Bye!")
            break
        else:
            print("Invalid choice! Please choose a number between 1–7.")

if __name__ == "__main__":
    main()
