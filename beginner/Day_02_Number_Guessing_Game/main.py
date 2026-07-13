import tkinter as tk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 2: Number Guessing Game")
        self.root.geometry("400x350")
        self.root.configure(bg="#121212")  # 60% Black Dominant Background
        self.root.resizable(False, False)

        # Game State
        self.target_number = 0
        self.attempts = 0
        
        # Header Label
        self.header_label = tk.Label(
            self.root, 
            text="NUMBER GUESSER", 
            font=("Helvetica", 16, "bold"), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue
        )
        self.header_label.pack(pady=20)

        # Instruction Label
        self.inst_label = tk.Label(
            self.root, 
            text="Guess a number between 1 and 100:", 
            font=("Helvetica", 11), 
            bg="#121212", 
            fg="#FFFFFF"  # 10% White
        )
        self.inst_label.pack(pady=5)

        # Entry (Secondary color container style)
        self.entry = tk.Entry(
            self.root, 
            font=("Helvetica", 14, "bold"), 
            justify="center", 
            bg="#1E3A8A", 
            fg="#FFFFFF", 
            insertbackground="#FFFFFF", 
            bd=0,
            width=10
        )
        self.entry.pack(pady=10)

        # Submit Button
        self.submit_btn = tk.Button(
            self.root, 
            text="Submit Guess", 
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A", 
            fg="#FFFFFF", 
            activebackground="#2563EB", 
            activeforeground="#FFFFFF", 
            bd=0, 
            padx=15, 
            pady=6, 
            command=self.check_guess,
            cursor="hand2"
        )
        self.submit_btn.pack(pady=10)

        # Feedback Label
        self.feedback_label = tk.Label(
            self.root, 
            text="Good luck!", 
            font=("Helvetica", 12, "italic"), 
            bg="#121212", 
            fg="#FFFFFF"
        )
        self.feedback_label.pack(pady=15)

        # Restart Button
        self.restart_btn = tk.Button(
            self.root, 
            text="Play Again", 
            font=("Helvetica", 9, "bold"),
            bg="#121212", 
            fg="#1E3A8A", 
            activebackground="#121212", 
            activeforeground="#2563EB", 
            bd=0, 
            padx=10, 
            pady=4, 
            command=self.reset_game,
            cursor="hand2"
        )
        
        # Start game
        self.reset_game()

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        if hasattr(self, 'entry'):
            self.entry.config(state="normal")
            self.entry.delete(0, tk.END)
            self.feedback_label.config(text="Good luck!", fg="#FFFFFF")
            self.submit_btn.config(state="normal")
            self.restart_btn.pack_forget()

    def check_guess(self):
        guess_str = self.entry.get().strip()
        if not guess_str.isdigit():
            self.feedback_label.config(text="Please enter a valid integer!", fg="#EF4444")
            return
        
        guess = int(guess_str)
        self.attempts += 1

        if guess < self.target_number:
            self.feedback_label.config(text=f"Too low! Attempts: {self.attempts}", fg="#FFFFFF")
            self.entry.delete(0, tk.END)
        elif guess > self.target_number:
            self.feedback_label.config(text=f"Too high! Attempts: {self.attempts}", fg="#FFFFFF")
            self.entry.delete(0, tk.END)
        else:
            self.feedback_label.config(text=f"Correct! You got it in {self.attempts} attempts!", fg="#10B981")
            self.entry.config(state="disabled")
            self.submit_btn.config(state="disabled")
            self.restart_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
