import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pandas as pd
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df


class ClassroomSchedule:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Classroom Schedule Management")
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Classroom Scheduling Dashboard", font=("Helvetica", 16)).pack(pady=10)

        self.schedule_list = tk.Listbox(self.root, height=10)
        self.schedule_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.root, text="Book Classroom", command=self.open_booking_window).pack(pady=5)
        tk.Button(self.root, text="View Calendar", command=self.open_calendar_view).pack(pady=5)
        tk.Button(self.root, text="Refresh", command=self.refresh_schedules).pack(pady=5)
        tk.Button(self.root, text="Close", command=self.root.destroy).pack(pady=5)

        self.refresh_schedules()

    def refresh_schedules(self):
        try:
            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df['end_time'] = pd.to_datetime(schedules_df['end_time'], errors='coerce')

            schedules_df = schedules_df.dropna(subset=['start_time', 'end_time'])

            self.schedule_list.delete(0, tk.END)

            for _, schedule in schedules_df.iterrows():
                reserved_by = f"{schedule['reserved_by']}"  # Adjusted for combobox changes
                self.schedule_list.insert(
                    tk.END,
                    f"{schedule['classroom_name']} | {schedule['start_time']} - {schedule['end_time']} | Reserved by: {reserved_by} | Purpose: {schedule['purpose']}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh schedules: {e}")

    def open_booking_window(self):
        BookClassroom(self.refresh_schedules)

    def open_calendar_view(self):
        CalendarView()


class BookClassroom:
    def __init__(self, refresh_callback):
        self.refresh_callback = refresh_callback
        self.root = tk.Toplevel()
        self.root.title("Book Classroom")
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Classroom Name:").grid(row=0, column=0, padx=10, pady=5)
        self.classroom_name_combobox = ttk.Combobox(self.root, values=self.get_classroom_names())
        self.classroom_name_combobox.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Date:").grid(row=1, column=0, padx=10, pady=5)
        self.date_combobox = ttk.Combobox(self.root, values=self.get_date_options())
        self.date_combobox.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Start Time:").grid(row=2, column=0, padx=10, pady=5)
        self.start_hour_combobox = ttk.Combobox(self.root, values=self.get_hour_options(), width=5)
        self.start_hour_combobox.grid(row=2, column=1, padx=5, sticky="w")
        self.start_minute_combobox = ttk.Combobox(self.root, values=self.get_minute_options(), width=5)
        self.start_minute_combobox.grid(row=2, column=1, padx=5, sticky="e")

        tk.Label(self.root, text="End Time:").grid(row=3, column=0, padx=10, pady=5)
        self.end_hour_combobox = ttk.Combobox(self.root, values=self.get_hour_options(), width=5)
        self.end_hour_combobox.grid(row=3, column=1, padx=5, sticky="w")
        self.end_minute_combobox = ttk.Combobox(self.root, values=self.get_minute_options(), width=5)
        self.end_minute_combobox.grid(row=3, column=1, padx=5, sticky="e")

        tk.Label(self.root, text="Reserved By:").grid(row=4, column=0, padx=10, pady=5)
        self.reserved_by_combobox = ttk.Combobox(self.root, values=self.get_reserved_by_names())
        self.reserved_by_combobox.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Purpose:").grid(row=5, column=0, padx=10, pady=5)
        self.purpose_entry = tk.Entry(self.root)
        self.purpose_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Submit", command=self.book_classroom).grid(row=6, column=1, pady=10)

    def get_classroom_names(self):
        try:
            schedules_df = read_from_df('classroom_schedules')
            return schedules_df['classroom_name'].unique().tolist()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch classroom names: {e}")
            return []

    def get_date_options(self):
        today = datetime.now()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    def get_hour_options(self):
        return [f"{i:02}" for i in range(24)]

    def get_minute_options(self):
        return [f"{i:02}" for i in range(0, 60, 5)]

    def get_reserved_by_names(self):
        try:
            students_df = read_from_df('students')
            teachers_df = read_from_df('teachers')

            reserved_by_names = students_df.apply(lambda row: f"{row['first_name']} {row['last_name']}", axis=1).tolist()
            reserved_by_names.extend(
                teachers_df.apply(lambda row: f"{row['first_name']} {row['last_name']}", axis=1).tolist()
            )
            return reserved_by_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch reserved_by names: {e}")
            return []

    def book_classroom(self):
        try:
            classroom_name = self.classroom_name_combobox.get()
            date = self.date_combobox.get()
            start_time = f"{date} {self.start_hour_combobox.get()}:{self.start_minute_combobox.get()}"
            end_time = f"{date} {self.end_hour_combobox.get()}:{self.end_minute_combobox.get()}"
            reserved_by = self.reserved_by_combobox.get()
            purpose = self.purpose_entry.get()

            start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

            if not classroom_name or not reserved_by or not purpose:
                messagebox.showerror("Error", "All fields are required!")
                return

            if start_datetime >= end_datetime:
                messagebox.showerror("Error", "End time must be after start time.")
                return

            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df['end_time'] = pd.to_datetime(schedules_df['end_time'], errors='coerce')

            overlapping = schedules_df[
                (schedules_df['classroom_name'] == classroom_name) &
                ((schedules_df['start_time'] < end_datetime) & (schedules_df['end_time'] > start_datetime))
            ]

            if not overlapping.empty:
                messagebox.showerror("Error", "Scheduling conflict detected!")
                return

            new_booking = pd.DataFrame([{
                "classroom_name": classroom_name,
                "start_time": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "reserved_by": reserved_by,
                "purpose": purpose
            }])

            schedules_df = pd.concat([schedules_df, new_booking], ignore_index=True)

            save_df_to_db('classroom_schedules', schedules_df)

            messagebox.showinfo("Success", "Classroom booked successfully!")
            self.refresh_callback()
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book classroom: {e}")


class CalendarView:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Classroom Calendar View")
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Classroom Schedule - Calendar View", font=("Helvetica", 16)).pack(pady=10)

        self.calendar = Calendar(self.root, selectmode="day", year=datetime.now().year, month=datetime.now().month)
        self.calendar.pack(pady=10)

        tk.Button(self.root, text="Show Events", command=self.show_events).pack(pady=5)

        self.events_list = tk.Listbox(self.root, height=10)
        self.events_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_events()

    def load_events(self):
        try:
            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df = schedules_df.dropna(subset=['start_time'])

            for _, schedule in schedules_df.iterrows():
                event_date = schedule['start_time'].date()
                self.calendar.calevent_create(event_date, schedule['purpose'], 'event')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load events: {e}")

    def show_events(self):
        try:
            selected_date = self.calendar.get_date()
            selected_date_obj = datetime.strptime(selected_date, "%m/%d/%y").date()

            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df['start_date'] = schedules_df['start_time'].dt.date
            schedules_df = schedules_df.dropna(subset=['start_time'])

            selected_events = schedules_df[schedules_df['start_date'] == selected_date_obj]

            self.events_list.delete(0, tk.END)
            for _, event in selected_events.iterrows():
                reserved_by = f"{event['reserved_by']}"
                event_info = f"{event['classroom_name']} | {event['start_time']} - {event['end_time']} | Reserved by: {reserved_by} | Purpose: {event['purpose']}"
                self.events_list.insert(tk.END, event_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show events: {e}")


if __name__ == "__main__":
    app = ClassroomSchedule()
    app.root.mainloop()
