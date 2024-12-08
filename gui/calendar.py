import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
from datetime import datetime
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
                self.schedule_list.insert(
                    tk.END,
                    f"{schedule['classroom_name']} | {schedule['start_time']} - {schedule['end_time']} | Reserved by: {schedule['reserved_by']}"
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
        self.classroom_name_entry = tk.Entry(self.root)
        self.classroom_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Start Time (YYYY-MM-DD HH:MM):").grid(row=1, column=0, padx=10, pady=5)
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="End Time (YYYY-MM-DD HH:MM):").grid(row=2, column=0, padx=10, pady=5)
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Reserved By:").grid(row=3, column=0, padx=10, pady=5)
        self.reserved_by_entry = tk.Entry(self.root)
        self.reserved_by_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Purpose:").grid(row=4, column=0, padx=10, pady=5)
        self.purpose_entry = tk.Entry(self.root)
        self.purpose_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Submit", command=self.book_classroom).grid(row=5, column=1, pady=10)

    def book_classroom(self):
        try:
            classroom_name = self.classroom_name_entry.get()
            start_time = datetime.strptime(self.start_time_entry.get(), "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(self.end_time_entry.get(), "%Y-%m-%d %H:%M")
            reserved_by = self.reserved_by_entry.get()
            purpose = self.purpose_entry.get()

            if not classroom_name or not reserved_by or not purpose:
                messagebox.showerror("Error", "All fields are required!")
                return

            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be after start time.")
                return

            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df['end_time'] = pd.to_datetime(schedules_df['end_time'], errors='coerce')

            overlapping = schedules_df[
                (schedules_df['classroom_name'] == classroom_name) &
                ((schedules_df['start_time'] < end_time) & (schedules_df['end_time'] > start_time))
            ]

            if not overlapping.empty:
                messagebox.showerror("Error", "Scheduling conflict detected!")
                return

            new_booking = pd.DataFrame([{
                "classroom_name": classroom_name,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "reserved_by": reserved_by,
                "purpose": purpose
            }])

            schedules_df = pd.concat([schedules_df, new_booking], ignore_index=True)

            save_df_to_db(
                table_name='classroom_schedules',
                dataframe=schedules_df,
                new=new_booking.to_dict(orient='records'),
                who="Teacher",
                index=None
            )

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
                event_info = f"{event['classroom_name']} | {event['start_time']} - {event['end_time']} | Purpose: {event['purpose']}"
                self.events_list.insert(tk.END, event_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show events: {e}")
