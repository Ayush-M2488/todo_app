# todo.py

import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Define the Task class
class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        """Convert the Task instance into a dictionary for JSON serialization."""
        return {
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        """Create a Task instance from a dictionary."""
        task = Task(data['title'], data['description'], data['category'])
        task.completed = data.get('completed', False)
        return task

# File Handling Functions
TASKS_FILE = 'tasks.json'

def save_tasks(tasks):
    """Save a list of Task instances to a JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)
    print("Tasks have been saved successfully.\n")

def load_tasks():
    """Load tasks from a JSON file and return a list of Task instances."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            tasks_data = json.load(f)
            return [Task.from_dict(task) for task in tasks_data]
        except json.JSONDecodeError:
            print("Error: Corrupted tasks.json file. Starting with an empty task list.\n")
            return []

# GUI Application Class
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List Application")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Load tasks
        self.tasks = load_tasks()

        # Setup GUI Components
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components."""
        # Frame for Task List
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=20)

        # Scrollbar for Task List
        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview for displaying tasks
        self.task_tree = ttk.Treeview(self.task_frame, columns=("Description", "Category", "Status"), show='headings', yscrollcommand=self.scrollbar.set)
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.column("Description", width=300)
        self.task_tree.column("Category", width=100)
        self.task_tree.column("Status", width=100)
        self.task_tree.pack()

        self.scrollbar.config(command=self.task_tree.yview)

        # Populate the task list
        self.populate_tasks()

        # Frame for Add Task
        self.add_task_frame = tk.Frame(self.root)
        self.add_task_frame.pack(pady=20)

        # Title Entry
        tk.Label(self.add_task_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.title_entry = tk.Entry(self.add_task_frame, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Description Entry
        tk.Label(self.add_task_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.description_entry = tk.Entry(self.add_task_frame, width=50)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category Dropdown
        tk.Label(self.add_task_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.add_task_frame, textvariable=self.category_var, state='readonly')
        self.category_dropdown['values'] = ("Work", "Personal", "Urgent", "Uncategorized")
        self.category_dropdown.current(3)  # Default to "Uncategorized"
        self.category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Add Task Button
        self.add_button = tk.Button(self.add_task_frame, text="Add Task", command=self.add_task, bg="#28a745", fg="white", width=20)
        self.add_button.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)

        # Frame for Action Buttons
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)

        # Mark Completed Button
        self.complete_button = tk.Button(self.action_frame, text="Mark as Completed", command=self.mark_completed, bg="#007bff", fg="white", width=20)
        self.complete_button.grid(row=0, column=0, padx=10)

        # Delete Task Button
        self.delete_button = tk.Button(self.action_frame, text="Delete Task", command=self.delete_task, bg="#dc3545", fg="white", width=20)
        self.delete_button.grid(row=0, column=1, padx=10)

        # Exit Button
        self.exit_button = tk.Button(self.action_frame, text="Exit", command=self.exit_app, bg="#6c757d", fg="white", width=20)
        self.exit_button.grid(row=0, column=2, padx=10)

    def populate_tasks(self):
        """Populate the Treeview with existing tasks."""
        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"
            self.task_tree.insert('', tk.END, values=(task.description, task.category, status))

    def add_task(self):
        """Add a new task to the list."""
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        category = self.category_var.get()

        if not title:
            messagebox.showwarning("Input Error", "Please enter a task title.")
            return

        if not description:
            messagebox.showwarning("Input Error", "Please enter a task description.")
            return

        if not category:
            category = "Uncategorized"

        new_task = Task(title, description, category)
        self.tasks.append(new_task)
        self.task_tree.insert('', tk.END, values=(new_task.description, new_task.category, "Pending"))

        # Clear input fields
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.category_dropdown.current(3)  # Reset to "Uncategorized"

        messagebox.showinfo("Success", f"Task '{title}' added successfully.")

    def mark_completed(self):
        """Mark the selected task as completed."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")
            return

        item = self.task_tree.item(selected_item)
        description = item['values'][0]

        for task in self.tasks:
            if task.description == description:
                if task.completed:
                    messagebox.showinfo("Info", f"Task '{task.title}' is already completed.")
                    return
                task.mark_completed()
                self.task_tree.item(selected_item, values=(task.description, task.category, "Completed"))
                messagebox.showinfo("Success", f"Task '{task.title}' marked as completed.")
                return

    def delete_task(self):
        """Delete the selected task from the list."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?")
        if not confirm:
            return

        item = self.task_tree.item(selected_item)
        description = item['values'][0]

        for idx, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[idx]
                self.task_tree.delete(selected_item)
                messagebox.showinfo("Success", f"Task '{task.title}' has been deleted.")
                return

    def exit_app(self):
        """Save tasks and exit the application."""
        save_tasks(self.tasks)
        self.root.destroy()

# Main function to run the application
def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_app)  # Handle window close button
    root.mainloop()

if __name__ == "__main__":
    main()
