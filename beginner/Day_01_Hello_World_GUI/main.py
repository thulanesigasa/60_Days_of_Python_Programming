import tkinter as tk

class HelloWorldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 1: Hello World GUI")
        self.root.geometry("400x300")
        self.root.configure(bg="#121212")  # 60% Black Dominant Background
        
        # Prevent resizing to keep design neat
        self.root.resizable(False, False)

        # Title/Header
        self.header_label = tk.Label(
            self.root, 
            text="Day 1 Project", 
            font=("Helvetica", 12, "bold"), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue
        )
        self.header_label.pack(pady=15)

        # Hello World Label
        self.hello_label = tk.Label(
            self.root, 
            text="Hello, World!", 
            font=("Helvetica", 28, "bold"), 
            bg="#121212", 
            fg="#FFFFFF"  # 10% White
        )
        self.hello_label.pack(expand=True)

        # Button (Secondary - 20% Blue container, 10% White text)
        self.exit_button = tk.Button(
            self.root, 
            text="Dismiss", 
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A", 
            fg="#FFFFFF", 
            activebackground="#2563EB", 
            activeforeground="#FFFFFF", 
            bd=0, 
            padx=20, 
            pady=8, 
            command=self.root.destroy,
            cursor="hand2"
        )
        self.exit_button.pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()
