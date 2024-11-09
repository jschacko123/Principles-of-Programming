import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, scrolledtext, messagebox
import re

# Import your existing lexer function here
# from lexer import lexical_analyzer  # Uncomment if lexer function is in a separate lexer.py file

# Define patterns for diffeent token types
token_patterns = [
    ("KEYWORD", r"\b(int|float|if|else|while|return|void|bool|char)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),
    ("OPERATOR", r"[+\-*/=<>!&|]"),
    ("PUNCTUATION", r"[;{},()]"),
]

def lexical_analyzer(source_code):
    tokens = []
    for token_type, pattern in token_patterns:
        for match in re.finditer(pattern, source_code):
            lexeme = match.group(0)
            tokens.append((token_type, lexeme))
    return tokens

# Function to load a file and display its content
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, content)

# Function to run the lexical analyzer and display results
def run_lexer():
    source_code = input_text.get(1.0, tk.END)
    if not source_code.strip():
        messagebox.showwarning("no input!", "please load or enter source code to analyze <3")
        return
    
    tokens = lexical_analyzer(source_code)
    result_text.delete(1.0, tk.END)  # clear previous results

    # Display tokens and lexemes
    for token_type, lexeme in tokens:
        result_text.insert(tk.END, f"Token: {token_type}, Lexeme: {lexeme}\n")

# setting up the GUI window using tkinter
window = tk.Tk()   

# setting the bkg color and title 
window.configure(bg="#f9baff")  
window.title("Fall 2024: Group 2 Programming Languages Lexical Analyzer GUI")

# setting the window width and height
window_width = 600
window_height = 600

# i want to center the window whenever it opens
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# calculate the center position of the window on the screen
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


  

# Input text area
label = tk.Label(window, text="source code:", font=("Helvetica", 10))  # Set font to Helvetica, size 12
label.pack(pady=2)
input_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=10)
input_text.pack(fill=tk.BOTH, expand=True)
input_text.config(bg="#fcdfff")  

# Define a custom style for rounded buttons
style = ttk.Style()
style.configure("Rounded.TButton", font=("Helvetica", 10), padding=2, relief="flat")
style.map("Rounded.TButton", background=[("active", "#d1d1e0")])

# Create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack(fill=tk.X, pady=2)

# Create rounded buttons using the custom style
load_button = ttk.Button(button_frame, text="load file", style="Rounded.TButton", command=load_file)
load_button.pack(side=tk.LEFT, padx=5, pady=5)

run_button = ttk.Button(button_frame, text="run lexer", style="Rounded.TButton", command=run_lexer)
run_button.pack(side=tk.LEFT, padx=5, pady=5)

# Result text area
label2 = tk.Label(window, text="tokens and lexemes:", font=("Helvetica", 10))
label2.pack(pady=2)
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=20)
result_text.pack(fill=tk.BOTH, expand=True)
result_text.config(bg="#fcdfff")


# Run the GUI loop
window.mainloop()
