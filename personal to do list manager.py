import logging

class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def __str__(self):\
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} - {status}, Due: {self.due_date}" if self.due_date else f"{self.description} - {status}"

class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.due_date = due_date
        return self

    def build(self):
        return self.task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []
        self.redo_stack = []

    def add_task(self, task):
        self.tasks.append(task)
        self.undo_stack.append(self.tasks.copy())
        logging.info(f"Task '{task.description}' added.")

    def mark_completed(self, description):
        task = next((t for t in self.tasks if t.description == description), None)
        if task:
            task.mark_completed()
            self.undo_stack.append(self.tasks.copy())
            logging.info(f"Task '{description}' marked as completed.")
        else:
            logging.warning(f"Task '{description}' not found.")

    def delete_task(self, description):
        self.tasks = [task for task in self.tasks if task.description != description]
        self.undo_stack.append(self.tasks.copy())
        logging.info(f"Task '{description}' deleted.")

    def view_tasks(self, filter_type=None):
        tasks_to_display = self.tasks if not filter_type else [task for task in self.tasks if
                                                               (filter_type == 'completed' and task.completed) or
                                                               (filter_type == 'pending' and not task.completed)]
        for task in tasks_to_display:
            logging.info(task)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.tasks = self.undo_stack[-1].copy()
            logging.info("Undo completed.")
        else:
            logging.warning("Undo not possible.")

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.tasks = self.undo_stack[-1].copy()
            logging.info("Redo completed.")
        else:
            logging.warning("Redo not possible.")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    manager = TaskManager()

    while True:
        user_input = input("Enter command (add, complete, delete, view, undo, redo, exit): ").split()
        try:
            command = user_input[0]
            if command == "add":
                description = user_input[1]
                due_date = user_input[3] if len(user_input) > 3 and user_input[2] == "Due:" else None
                task = TaskBuilder(description).set_due_date(due_date).build()
                manager.add_task(task)
            elif command == "complete":
                description = user_input[1]
                manager.mark_completed(description)
            elif command == "delete":
                description = user_input[1]
                manager.delete_task(description)
            elif command == "view":
                filter_type = user_input[1] if len(user_input) > 1 else None
                manager.view_tasks(filter_type)
            elif command == "undo":
                manager.undo()
            elif command == "redo":
                manager.redo()
            elif command == "exit":
                break
            else:
                logging.error("Invalid command.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
