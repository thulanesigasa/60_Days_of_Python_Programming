import tkinter as tk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 3: Calculator")
        self.root.geometry("350x450")
        self.root.configure(bg="#121212")  # 60% Black
        self.root.resizable(False, False)

        self.expression = ""

        # Display screen (Cobalt Blue Background, White Text)
        self.display_frame = tk.Frame(self.root, bg="#121212")
        self.display_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.display_label = tk.Label(
            self.display_frame, 
            text="", 
            anchor="e", 
            font=("Helvetica", 14), 
            bg="#121212", 
            fg="#1E3A8A"  # 20% Cobalt Blue Accent
        )
        self.display_label.pack(fill="x", pady=(10, 0))

        self.result_label = tk.Label(
            self.display_frame, 
            text="0", 
            anchor="e", 
            font=("Helvetica", 28, "bold"), 
            bg="#121212", 
            fg="#FFFFFF"  # 10% White Accent
        )
        self.result_label.pack(fill="x", pady=(0, 10))

        # Button grid frame
        self.buttons_frame = tk.Frame(self.root, bg="#121212")
        self.buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Buttons layout configuration
        buttons = [
            ['C', 'CE', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '']
        ]

        # Configure rows and columns weights
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1)

        for r, row in enumerate(buttons):
            for c, val in enumerate(row):
                if val == '':
                    continue
                # Style buttons: digits get dark gray, operators/special get blue
                if val in ['C', 'CE', '%', '/', '*', '-', '+', '=']:
                    bg_color = "#1E3A8A"
                    fg_color = "#FFFFFF"
                else:
                    bg_color = "#1E293B"
                    fg_color = "#FFFFFF"

                # Special spans
                colspan = 1
                if val == '0':
                    colspan = 2
                    c_pos = 0
                elif val == '.':
                    c_pos = 2
                elif val == '=':
                    c_pos = 3
                else:
                    c_pos = c

                btn = tk.Button(
                    self.buttons_frame,
                    text=val,
                    font=("Helvetica", 14, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#2563EB",
                    activeforeground="#FFFFFF",
                    bd=0,
                    relief="flat",
                    command=lambda v=val: self.on_button_press(v),
                    cursor="hand2"
                )
                btn.grid(row=r, column=c_pos, columnspan=colspan, sticky="nsew", padx=4, pady=4)

    def on_button_press(self, val):
        if val == 'C':
            self.expression = ""
            self.result_label.config(text="0")
            self.display_label.config(text="")
        elif val == 'CE':
            self.expression = self.expression[:-1]
            self.result_label.config(text=self.expression if self.expression else "0")
        elif val == '=':
            try:
                # Basic sanitation
                expr = self.expression.replace('%', '/100')
                result = str(eval(expr))
                # If result is floating point ending in .0, simplify to integer
                if result.endswith('.0'):
                    result = result[:-2]
                self.result_label.config(text=result)
                self.display_label.config(text=self.expression + " =")
                self.expression = result
            except ZeroDivisionError:
                self.result_label.config(text="Error: Div by 0")
                self.expression = ""
            except Exception:
                self.result_label.config(text="Error")
                self.expression = ""
        else:
            # Prevent double operators
            if val in ['+', '-', '*', '/', '%'] and (not self.expression or self.expression[-1] in ['+', '-', '*', '/', '%']):
                return
            self.expression += str(val)
            self.result_label.config(text=self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
