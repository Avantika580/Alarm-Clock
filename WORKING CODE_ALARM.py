
import tkinter as tk
from tkinter import messagebox
import datetime
import threading
import winsound

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("500x500")
        self.root.configure(bg='black')

        self.label = tk.Label(root, text="Set Alarm Time:", font=("Helvetica", 18, "bold"), bg='black', fg='orange')
        self.label.pack(pady=20)

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()

        self.hour_var.set("00")
        self.minute_var.set("00")

        self.time_frame = tk.Frame(root, bg='black')
        self.time_frame.pack(pady=10)

        self.hours = [str(i).zfill(2) for i in range(24)]
        self.minutes = [str(i).zfill(2) for i in range(60)]

        self.hour_dropdown = tk.OptionMenu(self.time_frame, self.hour_var, *self.hours)
        self.hour_dropdown.config(font=("Helvetica", 18), bg='black', fg='orange', bd=2, relief=tk.FLAT)
        self.hour_dropdown["menu"].config(bg='black', fg='orange')
        self.hour_dropdown.pack(side=tk.LEFT, padx=5)

        self.colon_label = tk.Label(self.time_frame, text=":", font=("Helvetica", 18), bg='black', fg='orange')
        self.colon_label.pack(side=tk.LEFT)

        self.minute_dropdown = tk.OptionMenu(self.time_frame, self.minute_var, *self.minutes)
        self.minute_dropdown.config(font=("Helvetica", 18), bg='black', fg='orange', bd=2, relief=tk.FLAT)
        self.minute_dropdown["menu"].config(bg='black', fg='orange')
        self.minute_dropdown.pack(side=tk.LEFT, padx=5)

        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm, font=("Helvetica", 14, "bold"), bg='orange', fg='black', bd=2, relief=tk.RAISED)
        self.set_button.pack(pady=20)

        self.days_frame = tk.LabelFrame(root, text="Days", font=("Helvetica", 18, "bold"), bg='black', fg='orange')
        self.days_frame.pack(pady=20)

        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_vars = []

        for i, day in enumerate(self.days):
            var = tk.IntVar()
            check_button = tk.Checkbutton(self.days_frame, text=day, variable=var, font=("Helvetica", 14), bg='black', fg='orange', selectcolor='orange')
            check_button.grid(row=0, column=i, padx=5, pady=5)
            self.day_vars.append(var)

        self.alarms_listbox = tk.Listbox(root, font=("Helvetica", 14), width=50, height=10, bd=2, relief=tk.FLAT, bg='black', fg='orange')
        self.alarms_listbox.pack(pady=20)

        self.alarms = []

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError

            selected_days = [self.days[i] for i, var in enumerate(self.day_vars) if var.get()]

            if not selected_days:
                messagebox.showerror("Error", "Please select at least one day.")
                return

            now = datetime.datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            for day in selected_days:
                day_index = self.days.index(day)
                day_difference = (day_index - now.weekday() + 7) % 7
                alarm_time += datetime.timedelta(days=day_difference)
                if alarm_time < now:
                    alarm_time += datetime.timedelta(days=7)

                time_diff = alarm_time - now
                threading.Timer(time_diff.total_seconds(), self.ring_alarm).start()
                self.alarms.append((alarm_time, day))
                alarm_time -= datetime.timedelta(days=day_difference)

            self.update_alarms_listbox()
            messagebox.showinfo("Alarm Set", "Alarm(s) set successfully.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid hour (0-23) and minute (0-59)")

    def update_alarms_listbox(self):
        self.alarms_listbox.delete(0, tk.END)
        for alarm in self.alarms:
            selected_days = ", ".join(day for i, day in enumerate(self.days) if self.day_vars[i].get())
            self.alarms_listbox.insert(tk.END, f"{selected_days}: {alarm[0].strftime('%A, %d %B %Y %I:%M %p')}")

    def ring_alarm(self):
        alarm_window = tk.Toplevel(self.root)
        alarm_window.title("Alarm!")
        alarm_window.geometry("400x350")
        alarm_window.configure(bg='black')

        alarm_label = tk.Label(alarm_window, text="Wake up!", font=("Helvetica", 24, "bold"), bg='black', fg='orange')
        alarm_label.pack(pady=20)

        dismiss_button = tk.Button(alarm_window, text="Dismiss", command=alarm_window.destroy, font=("Helvetica", 18, "bold"), bg='orange', fg='black', bd=2, relief=tk.RAISED)
        dismiss_button.pack(pady=10)

        snooze_button = tk.Button(alarm_window, text="Snooze", command=alarm_window.destroy, font=("Helvetica", 18, "bold"), bg='orange', fg='black', bd=2, relief=tk.RAISED)
        snooze_button.pack(pady=5)

        winsound.Beep(1000, 2000)  # Beep sound

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='black')
    alarm_clock = AlarmClock(root)
    root.mainloop()
