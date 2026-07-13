import tkinter as tk
from tkinter import messagebox
import os

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 4: To Do List App")
        self.root.geometry("400x480")
        self.root.configure(bg="#121212")  # 60% Black
        self.root.resizable(False, False)

        # File for persistence
        self.filename = os.path.join(os.path.dirname(__file__), "tasks.txt")

        # Header Label
        self.header_label = tk.Label(
            self.root, 
            text="MY TO-DO LIST", 
            font=("Helvetica", 16, "bold"), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue Accent
        )
        self.header_label.pack(pady=20)

        # Input Frame (Entry + Add Button)
        self.input_frame = tk.Frame(self.root, bg="#121212")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.task_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 12),
            bg="#1E293B",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            bd=0,
            relief="flat"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_btn = tk.Button(
            self.input_frame,
            text="Add Task",
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF",
            activebackground="#2563EB",
            activeforeground="#FFFFFF",
            bd=0,
            padx=15,
            command=self.add_task,
            cursor="hand2"
        )
        self.add_btn.pack(side="right", ipady=6)

        # Listbox Frame (Listbox + Scrollbar)
        self.list_frame = tk.Frame(self.root, bg="#121212")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.task_listbox = tk.Listbox(
            self.list_frame,
            font=("Helvetica", 11),
            bg="#1E293B",
            fg="#FFFFFF",
            selectbackground="#1E3A8A",
            selectforeground="#FFFFFF",
            bd=0,
            relief="flat",
            yscrollcommand=self.scrollbar.set
        )
        self.task_listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Action Buttons Frame
        self.actions_frame = tk.Frame(self.root, bg="#121212")
        self.actions_frame.pack(fill="x", padx=20, pady=20)

        self.delete_btn = tk.Button(
            self.actions_frame,
            text="Delete Selected Task",
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF",
            activebackground="#2563EB",
            activeforeground="#FFFFFF",
            bd=0,
            padx=10,
            pady=8,
            command=self.delete_task,
            cursor="hand2"
        )
        self.delete_btn.pack(fill="x")

        # Load existing tasks
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        self.task_listbox.insert(tk.END, task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()

    def delete_task(self):
        try:
            selected_idx = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_idx)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    for line in file:
                        task = line.strip()
                        if task:
                            self.task_listbox.insert(tk.END, task)
            except Exception as e:
                print(f"Error loading tasks: {e}")

    def save_tasks(self):
        try:
            with open(self.filename, "w") as file:
                tasks = self.task_listbox.get(0, tk.END)
                for task in tasks:
                    file.write(task + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
