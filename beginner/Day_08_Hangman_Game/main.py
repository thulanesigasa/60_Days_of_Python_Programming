import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 8: Hangman Game")
        self.root.geometry("600x550")
        self.root.configure(bg="#121212")  # 60% Black
        self.root.resizable(False, False)

        self.words = ["PYTHON", "DEVELOPER", "ANTIGRAVITY", "DATABASE", "APPLICATION", "KEYBOARD", "DISPLAY"]
        self.secret_word = ""
        self.guessed_letters = set()
        self.remaining_attempts = 6

        # Header Label
        self.header_label = tk.Label(
            self.root,
            text="HANGMAN GAME",
            font=("Helvetica", 16, "bold"),
            bg="#121212",
            fg="#1E3A8A"  # 20% Cobalt Blue
        )
        self.header_label.pack(pady=15)

        # Main horizontal panel: Left = Canvas, Right = Word Display & Game Controls
        self.game_panel = tk.Frame(self.root, bg="#121212")
        self.game_panel.pack(fill="both", expand=True, padx=20)

        # Canvas for drawing Hangman (Black Background, Blue lines)
        self.canvas = tk.Canvas(
            self.game_panel,
            width=250,
            height=280,
            bg="#1E293B",
            highlightthickness=2,
            highlightbackground="#1E3A8A"
        )
        self.canvas.pack(side="left", padx=(0, 20))

        self.info_panel = tk.Frame(self.game_panel, bg="#121212")
        self.info_panel.pack(side="right", fill="both", expand=True)

        self.word_label = tk.Label(
            self.info_panel,
            text="",
            font=("Consolas", 22, "bold"),
            bg="#121212",
            fg="#FFFFFF"  # 10% White
        )
        self.word_label.pack(pady=30)

        self.status_label = tk.Label(
            self.info_panel,
            text="Guesses remaining: 6",
            font=("Helvetica", 11, "bold"),
            bg="#121212",
            fg="#E2E8F0"
        )
        self.status_label.pack(pady=10)

        # Keyboard Frame (A-Z)
        self.keyboard_frame = tk.Frame(self.root, bg="#121212")
        self.keyboard_frame.pack(fill="x", padx=20, pady=20)

        self.buttons_dict = {}
        self.create_keyboard()

        # Restart Button
        self.restart_btn = tk.Button(
            self.info_panel,
            text="Play Again",
            font=("Helvetica", 10, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF",
            activebackground="#2563EB",
            activeforeground="#FFFFFF",
            bd=0,
            padx=15,
            pady=8,
            command=self.reset_game,
            cursor="hand2"
        )

        self.reset_game()

    def create_keyboard(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row_layouts = [
            alphabet[0:9],
            alphabet[9:18],
            alphabet[18:26]
        ]
        
        for r, letters in enumerate(row_layouts):
            row_frame = tk.Frame(self.keyboard_frame, bg="#121212")
            row_frame.pack(pady=3)
            for letter in letters:
                btn = tk.Button(
                    row_frame,
                    text=letter,
                    font=("Helvetica", 10, "bold"),
                    width=4,
                    height=1,
                    bg="#1E3A8A",
                    fg="#FFFFFF",
                    activebackground="#2563EB",
                    activeforeground="#FFFFFF",
                    bd=0,
                    relief="flat",
                    command=lambda l=letter: self.guess_letter(l),
                    cursor="hand2"
                )
                btn.pack(side="left", padx=3)
                self.buttons_dict[letter] = btn

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters.clear()
        self.remaining_attempts = 6
        self.status_label.config(text="Guesses remaining: 6", fg="#E2E8F0")
        self.restart_btn.pack_forget()
        
        # Clear Canvas and draw base gallows
        self.canvas.delete("all")
        self.canvas.create_line(30, 250, 220, 250, fill="#1E3A8A", width=4)
        self.canvas.create_line(80, 250, 80, 40, fill="#1E3A8A", width=4)
        self.canvas.create_line(80, 40, 160, 40, fill="#1E3A8A", width=4)
        self.canvas.create_line(160, 40, 160, 70, fill="#1E3A8A", width=4)

        # Enable all buttons
        for btn in self.buttons_dict.values():
            btn.config(state="normal", bg="#1E3A8A", fg="#FFFFFF")

        self.update_word_display()

    def update_word_display(self):
        display_word = " ".join([char if char in self.guessed_letters else "_" for char in self.secret_word])
        self.word_label.config(text=display_word)

    def guess_letter(self, letter):
        self.guessed_letters.add(letter)
        self.buttons_dict[letter].config(state="disabled", bg="#1E293B", fg="#64748B")

        if letter in self.secret_word:
            self.update_word_display()
            if all(char in self.guessed_letters for char in self.secret_word):
                self.status_label.config(text="Congratulations! You Won!", fg="#10B981")
                self.end_game()
        else:
            self.remaining_attempts -= 1
            self.status_label.config(text=f"Guesses remaining: {self.remaining_attempts}", fg="#EF4444")
            self.draw_hangman()
            if self.remaining_attempts == 0:
                self.status_label.config(text="Game Over!", fg="#EF4444")
                self.word_label.config(text=f"Word: {self.secret_word}")
                self.end_game()

    def end_game(self):
        for btn in self.buttons_dict.values():
            btn.config(state="disabled")
        self.restart_btn.pack(pady=15)

    def draw_hangman(self):
        if self.remaining_attempts == 5:
            self.canvas.create_oval(140, 70, 180, 110, outline="#1E3A8A", fill="#1E293B", width=3)
        elif self.remaining_attempts == 4:
            self.canvas.create_line(160, 110, 160, 180, fill="#1E3A8A", width=3)
        elif self.remaining_attempts == 3:
            self.canvas.create_line(160, 130, 130, 150, fill="#1E3A8A", width=3)
        elif self.remaining_attempts == 2:
            self.canvas.create_line(160, 130, 190, 150, fill="#1E3A8A", width=3)
        elif self.remaining_attempts == 1:
            self.canvas.create_line(160, 180, 135, 220, fill="#1E3A8A", width=3)
        elif self.remaining_attempts == 0:
            self.canvas.create_line(160, 180, 185, 220, fill="#1E3A8A", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
