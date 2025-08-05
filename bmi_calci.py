import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('bmi_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_bmi_record(username, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_app.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bmi_records (username, date, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), weight, height, bmi, category))
    conn.commit()
    conn.close()

def get_bmi_records(username):
    conn = sqlite3.connect('bmi_app.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, bmi FROM bmi_records WHERE username=? ORDER BY date
    ''', (username,))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- BMI Functions ----------
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ---------- GUI Application ----------
class BMIGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced BMI Calculator")
        self.geometry("420x470")
        self.configure(bg="#f2f2f2")
        self.username = None
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self, padding=20)
        self.login_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        ttk.Label(self.login_frame, text="User Login", font=("Arial", 16, 'bold')).pack(pady=(0, 15))
        ttk.Label(self.login_frame, text="Enter your username:").pack()
        self.username_entry = ttk.Entry(self.login_frame, width=25)
        self.username_entry.pack(pady=5)
        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=15)

    def login(self):
        uname = self.username_entry.get().strip()
        if not uname:
            messagebox.showerror("Error", "Please enter a username.")
            return
        self.username = uname
        self.login_frame.destroy()
        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self, padding=20, style="Main.TFrame")
        self.main_frame.place(relx=0.5, rely=0.02, anchor='n')

        ttk.Label(self.main_frame, text=f"Welcome, {self.username}!", font=("Arial", 15, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0,15))

        ttk.Label(self.main_frame, text="Weight (kg):").grid(row=1, column=0, sticky="e")
        self.weight_entry = ttk.Entry(self.main_frame, width=15)
        self.weight_entry.grid(row=1, column=1, pady=3)

        ttk.Label(self.main_frame, text="Height (m):").grid(row=2, column=0, sticky="e")
        self.height_entry = ttk.Entry(self.main_frame, width=15)
        self.height_entry.grid(row=2, column=1, pady=3)

        ttk.Button(self.main_frame, text="Calculate BMI", command=self.process_bmi).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 13), bg="#f2f2f2")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=8)

        ttk.Separator(self.main_frame, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', pady=12)
        ttk.Button(self.main_frame, text="Show BMI History", command=self.show_bmi_history, width=20).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(self.main_frame, text="Exit", command=self.quit, width=20).grid(row=7, column=0, columnspan=2, pady=3)

    def process_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not (20 <= weight <= 300):
                raise ValueError("Weight out of reasonable range.")
            if not (0.8 <= height <= 2.5):
                raise ValueError("Height out of reasonable range.")
        except Exception as e:
            self.result_label.configure(text=f"Error: {e}", fg="red")
            return
        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)
        color = {"Underweight": "#007EC6", "Normal": "#0DA96B", "Overweight": "#FFB300", "Obese": "#D7263D"}[category]
        self.result_label.configure(text=f"BMI: {bmi}   ({category})", fg=color)
        save_bmi_record(self.username, weight, height, bmi, category)

    def show_bmi_history(self):
        records = get_bmi_records(self.username)
        if not records:
            messagebox.showinfo("No Data", "No BMI history found for this user.")
            return
        dates = [r[0] for r in records]
        bmis = [r[1] for r in records]
        plt.figure(figsize=(8, 4))
        plt.plot(dates, bmis, marker='o', color='#007EC6')
        plt.title(f"{self.username}'s BMI History")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(True, alpha=0.3)
        plt.show()


if __name__ == "__main__":
    init_db()
    app = BMIGUI()
    app.mainloop()
