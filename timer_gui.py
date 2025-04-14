import tkinter as tk
from tkinter import messagebox
import threading
import time

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        self.total_seconds = 0
        self.remaining_seconds = 0
        self.paused = False
        self.running = False

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter time:", font=("Helvetica", 12)).pack(pady=10)

        self.time_entry = tk.Entry(self.root, font=("Helvetica", 14), justify='center')
        self.time_entry.pack()

        self.unit_var = tk.StringVar(value="seconds")
        tk.OptionMenu(self.root, self.unit_var, "seconds", "minutes").pack(pady=5)

        # Buttons
        self.start_button = tk.Button(self.root, text="Start", width=10, command=self.start_timer)
        self.pause_button = tk.Button(self.root, text="Pause", width=10, command=self.pause_timer, state='disabled')
        self.resume_button = tk.Button(self.root, text="Resume", width=10, command=self.resume_timer, state='disabled')

        self.start_button.pack(pady=5)
        self.pause_button.pack(pady=5)
        self.resume_button.pack(pady=5)

        self.time_display = tk.Label(self.root, text="", font=("Helvetica", 24), fg="blue")
        self.time_display.pack(pady=10)

    def start_timer(self):
        try:
            user_input = float(self.time_entry.get())
            unit = self.unit_var.get()

            self.total_seconds = int(user_input * 60) if unit == "minutes" else int(user_input)
            self.remaining_seconds = self.total_seconds

            if self.total_seconds <= 0:
                raise ValueError

            self.paused = False
            self.running = True
            self.update_button_states(started=True)
            threading.Thread(target=self.countdown, daemon=True).start()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number.")

    def countdown(self):
        while self.remaining_seconds > 0 and self.running:
            if not self.paused:
                mins, secs = divmod(self.remaining_seconds, 60)
                self.time_display.config(text=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                self.remaining_seconds -= 1
            else:
                time.sleep(0.1)

        if self.remaining_seconds == 0 and self.running:
            self.time_display.config(text="00:00")
            self.running = False
            self.update_button_states(finished=True)
            messagebox.showinfo("Time's Up", "⏰ Your countdown has finished!")

    def pause_timer(self):
        self.paused = True
        self.update_button_states(paused=True)

    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            self.update_button_states(resumed=True)

    def update_button_states(self, started=False, paused=False, resumed=False, finished=False):
        if started:
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.resume_button.config(state='disabled')
        elif paused:
            self.pause_button.config(state='disabled')
            self.resume_button.config(state='normal')
        elif resumed:
            self.pause_button.config(state='normal')
            self.resume_button.config(state='disabled')
        elif finished:
            self.start_button.config(state='normal')
            self.pause_button.config(state='disabled')
            self.resume_button.config(state='disabled')

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
