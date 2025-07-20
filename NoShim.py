"""
NoShim – A Lock Decoding Utility by B.S. Supply Co.
Modernized GUI with responsive layout and lively dark theme.
"""

import tkinter as tk
from tkinter import ttk, messagebox

def normalize(n):
    return n % 40

def get_mod_matches(base, r):
    return [normalize(base + i * 10) for i in range(4) if normalize(base + i * 10) % 4 == r]

def generate_second_digit_candidates(r):
    top_row = [normalize(r + 2 + 8 * i) for i in range(5)]
    bottom_row = [normalize(r + 6 + 8 * i) for i in range(5)]
    return top_row + bottom_row

def filter_close_pairs(second_digits, third_digit):
    return [v for v in second_digits if abs((v - third_digit) % 40) >= 2 and abs((third_digit - v) % 40) >= 2]

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.configure(bg="#1e1e2e")
    sw, sh = splash.winfo_screenwidth(), splash.winfo_screenheight()
    splash.geometry(f"320x120+{(sw - 320)//2}+{(sh - 120)//2}")
    label = tk.Label(splash, text="🔐 NoShim\nby B.S. Supply Co.",
                     font=("Segoe UI", 16, "bold"),
                     bg="#1e1e2e", fg="#5eead4")
    label.pack(expand=True)
    splash.after(1000, splash.destroy)
    splash.update()
    return splash

def calculate_candidates():
    try:
        sticky = int(entry_sticky.get())
        g1 = int(entry_g1.get())
        g2 = int(entry_g2.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    global third_candidate_list, r_value, first_digit
    first_digit = normalize(sticky + 5)
    r_value = first_digit % 4
    g1_matches = get_mod_matches(g1, r_value)
    g2_matches = get_mod_matches(g2, r_value)
    third_candidate_list = sorted(list(set(g1_matches + g2_matches)))

    combo_picker['values'] = third_candidate_list
    combo_picker.current(0)
    result_label.config(text=f"First digit: {first_digit}    Remainder: {r_value}")

def calculate_combos():
    if not third_candidate_list:
        messagebox.showerror("Missing Step", "Please calculate candidates first.")
        return
    try:
        third = int(combo_picker.get())
    except:
        messagebox.showerror("Input Error", "Please select a valid third digit.")
        return
    second_candidates = generate_second_digit_candidates(r_value)
    valid_seconds = filter_close_pairs(second_candidates, third)

    output_box.config(state='normal')
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, f"First: {first_digit}\nThird: {third}\n\nFinal combinations:\n")
    for v in valid_seconds:
        output_box.insert(tk.END, f"{first_digit}-{v}-{third}\n")
    output_box.config(state='disabled')

# App Setup
root = tk.Tk()
root.title("NoShim – B.S. Supply Co.")
root.configure(bg="#1e1e2e")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", foreground="#e0e0e0", background="#1e1e2e", font=("Segoe UI", 10))
style.configure("TEntry", foreground="#e0e0e0", fieldbackground="#313244", background="#1e1e2e")
style.configure("TCombobox", foreground="#e0e0e0", fieldbackground="#313244", background="#1e1e2e")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.map("TButton", background=[('active', '#5eead4')])

# Grid layout: responsive
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

ttk.Label(root, text="NoShim – A B.S. Supply Co. Project", font=("Segoe UI", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=(10, 0))

ttk.Label(root, text="Sticky Number:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
ttk.Label(root, text="Guess #1 (1–11):").grid(row=2, column=0, sticky='e', padx=5)
ttk.Label(root, text="Guess #2 (1–11):").grid(row=3, column=0, sticky='e', padx=5)

entry_sticky = ttk.Entry(root)
entry_g1 = ttk.Entry(root)
entry_g2 = ttk.Entry(root)

entry_sticky.grid(row=1, column=1, sticky='ew', padx=5)
entry_g1.grid(row=2, column=1, sticky='ew', padx=5)
entry_g2.grid(row=3, column=1, sticky='ew', padx=5)

ttk.Button(root, text="Find 3rd Digit Options", command=calculate_candidates).grid(row=4, column=0, columnspan=2, pady=8)

result_label = ttk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2)

combo_picker = ttk.Combobox(root, state="readonly")
combo_picker.grid(row=6, column=0, columnspan=2, padx=10, sticky="ew")

ttk.Button(root, text="Final Combos", command=calculate_combos).grid(row=7, column=0, columnspan=2, pady=8)

output_box = tk.Text(root, wrap="word", bg="#1e1e2e", fg="#e0e0e0", insertbackground="#5eead4",
                     font=("Consolas", 10), relief="flat")
output_box.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
output_box.config(state='disabled')

# Vars
third_candidate_list = []
first_digit = 0
r_value = 0

# Show splash and launch
splash = show_splash()
root.after(100, splash.destroy)

try:
    root.mainloop()
except Exception as e:
    import traceback
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())
    messagebox.showerror("Crash", "An error occurred. See error_log.txt.")
