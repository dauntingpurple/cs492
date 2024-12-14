import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
from src.saveChangeToDatabase import save_df_to_db, read_from_df


class ClassroomSchedule:
    def __init__(self, parent):
        """
        Initialize the Classroom Schedule Management GUI within the parent frame.
        """
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.parent, text="Classroom Scheduling Dashboard", font=("Helvetica", 16)).pack(pady=10)

        self.schedule_list = tk.Listbox(self.parent, height=10)
        self.schedule_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.parent, text="Book Classroom", command=self.open_booking_window).pack(pady=5)
        tk.Button(self.parent, text="View Calendar", command=self.open_calendar_view).pack(pady=5)
        tk.Button(self.parent, text="Refresh", command=self.refresh_schedules).pack(pady=5)

        self.refresh_schedules()

    def refresh_schedules(self):
        """
        Refresh the schedule list to display all classroom bookings.
        """
        try:
            schedules_df = read_from_df('classroom_schedules')

            schedules_df['start_time'] = pd.to_datetime(schedules_df['start_time'], errors='coerce')
            schedules_df['end_time'] = pd.to_datetime(schedules_df['end_time'], errors='coerce')

            schedules_df = schedules_df.dropna(subset=['start_time', 'end_time'])

            self.schedule_list.delete(0, tk.END)

            for _, schedule in schedules_df.iterrows():
                self.schedule_list.insert(
                    tk.END,
                    f"{schedule['classroom_name']} | {schedule['start_time']} - {schedule['end_time']} | Reserved by: {schedule['reserved_by']} | Purpose: {schedule['purpose']}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh schedules: {e}")

    def open_booking_window(self):
        """
        Open the booking window for scheduling classrooms.
        """
        BookingWindow(self.refresh_schedules)

    def open_calendar_view(self):
        """
        Open a calendar view to visualize classroom schedules.
        """
        CalendarView()


class BookingWindow:
    def __init__(self, refresh_callback):
        """
        Initialize the booking window for classroom scheduling.
        """
        self.refresh_callback = refresh_callback
        self.root = tk.Toplevel()
        self.root.title("Book Classroom")
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Classroom Name:").grid(row=0, column=0, padx=10, pady=5)
        self.classroom_name_combobox = ttk.Combobox(self.root, values=self.get_classroom_names())
        self.classroom_name_combobox.grid(row=0, column=1, columnspan=3, padx=10, pady=5)
        
        # Time and day values to populate
        today = datetime.today()
        year_values = [today.year + x for x in range(11)]  # Current year + next 10 years
        month_values = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']  # Two-digit month values
        day_values = [x for x in range(1, 32)]  # Days 1-31
        hour_values = [x for x in range(1, 13)]  # Hours 1-12
        minute_values = [x for x in range(0, 60, 5)]  # Minutes 0, 5, 10, ..., 55

        # Set default values
        default_day = today.day
        default_month = today.month
        default_year = today.year
        default_hour = today.hour % 12 or 12  # Convert 0 hour to 12
        default_minute = (today.minute // 5) * 5  # Round down to nearest 5
        default_am_pm = 'AM' if today.hour < 12 else 'PM'

        tk.Label(self.root, text="Start Date:").grid(row=1, column=0, padx=10, pady=5)
        self.start_date_MM_entry = ttk.Combobox(self.root, values=month_values, width=3)
        self.start_date_MM_entry.grid(row=1, column=1, padx=0, pady=5)
        self.start_date_MM_entry.set(f"{default_month:02}")  # Set default month
        self.start_date_DD_entry = ttk.Combobox(self.root, values=day_values, width=3)
        self.start_date_DD_entry.grid(row=1, column=2, padx=0, pady=5)
        self.start_date_DD_entry.set(f"{default_day:02}")  # Set default day
        self.start_date_YYYY_entry = ttk.Combobox(self.root, values=year_values, width=5)
        self.start_date_YYYY_entry.grid(row=1, column=3, padx=0, pady=5)
        self.start_date_YYYY_entry.set(str(default_year))  # Set default year

        tk.Label(self.root, text="End Time:").grid(row=2, column=0, padx=10, pady=5)
        self.end_date_MM_entry = ttk.Combobox(self.root, values=month_values, width=3)
        self.end_date_MM_entry.grid(row=2, column=1, padx=0, pady=5)
        self.end_date_MM_entry.set(f"{default_month:02}")  # Set default month
        self.end_date_DD_entry = ttk.Combobox(self.root, values=day_values, width=3)
        self.end_date_DD_entry.grid(row=2, column=2, padx=0, pady=5)
        self.end_date_DD_entry.set(f"{default_day:02}")  # Set default day
        self.end_date_YYYY_entry = ttk.Combobox(self.root, values=year_values, width=5)
        self.end_date_YYYY_entry.grid(row=2, column=3, padx=0, pady=5)
        self.end_date_YYYY_entry.set(str(default_year))  # Set default year

        tk.Label(self.root, text="Start Time:").grid(row=3, column=0, padx=10, pady=5)
        self.start_time_HH_entry = ttk.Combobox(self.root, values=hour_values, width=3)
        self.start_time_HH_entry.grid(row=3, column=1, padx=0, pady=5)
        self.start_time_HH_entry.set(str(default_hour))  # Set default hour
        self.start_time_MM_entry = ttk.Combobox(self.root, values=minute_values, width=3)
        self.start_time_MM_entry.grid(row=3, column=2, padx=0, pady=5)
        self.start_time_MM_entry.set(str(default_minute))  # Set default minute
        self.start_time_AM_entry = ttk.Combobox(self.root, values=['AM', 'PM'], width=5)
        self.start_time_AM_entry.grid(row=3, column=3, padx=0, pady=5)
        self.start_time_AM_entry.set(default_am_pm)  # Set default AM/PM

        tk.Label(self.root, text="End Time:").grid(row=4, column=0, padx=10, pady=5)
        self.end_time_HH_entry = ttk.Combobox(self.root, values=hour_values, width=3)
        self.end_time_HH_entry.grid(row=4, column=1, padx=0, pady=5)
        self.end_time_HH_entry.set(str(default_hour))  # Set default hour
        self.end_time_MM_entry = ttk.Combobox(self.root, values=minute_values, width=3)
        self.end_time_MM_entry.grid(row=4, column=2, padx=0, pady=5)
        self.end_time_MM_entry.set(str(default_minute))  # Set default minute
        self.end_time_PM_entry = ttk.Combobox(self.root, values=['AM', 'PM'], width=5)
        self.end_time_PM_entry.grid(row=4, column=3, padx=0, pady=5)
        self.end_time_PM_entry.set(default_am_pm)  # Set default AM/PM

        tk.Label(self.root, text="Reserved By:").grid(row=5, column=0, padx=10, pady=5)
        self.reserved_by_combobox = ttk.Combobox(self.root, values=self.get_reserved_by_names())
        self.reserved_by_combobox.grid(row=5, column=1, columnspan=3, padx=10, pady=5)

        tk.Label(self.root, text="Purpose:").grid(row=6, column=0, padx=10, pady=5)
        self.purpose_entry = tk.Entry(self.root)
        self.purpose_entry.grid(row=6, column=1, columnspan=3, padx=10, pady=5)

        tk.Button(self.root, text="Submit", command=self.book_classroom).grid(row=7, column=1, pady=10)

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
        return [f"{i:02d}" for i in range(24)]

    def get_minute_options(self):
        return [f"{i:02d}" for i in range(0, 60, 5)]

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
            start_date = f"{self.start_date_YYYY_entry.get()}-{self.start_date_MM_entry.get()}-{self.start_date_DD_entry.get()} {self.start_time_HH_entry.get()}:{self.start_time_MM_entry.get()} {self.start_time_AM_entry.get()}"
            end_date = f"{self.end_date_YYYY_entry.get()}-{self.end_date_MM_entry.get()}-{self.end_date_DD_entry.get()} {self.end_time_HH_entry.get()}:{self.end_time_MM_entry.get()} {self.end_time_PM_entry.get()}"
            start_time = datetime.strptime(start_date, "%Y-%m-%d %I:%M %p")
            end_time = datetime.strptime(end_date, "%Y-%m-%d %I:%M %p")

            reserved_by = self.reserved_by_combobox.get()
            purpose = self.purpose_entry.get()

            if not classroom_name or not reserved_by or not purpose:
                messagebox.showerror("Error", "All fields are required!")
                return

            start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            if start_dt >= end_dt:
                messagebox.showerror("Error", "End time must be after start time.")
                return

            schedules_df = read_from_df('classroom_schedules')
            overlapping = schedules_df[
                (schedules_df['classroom_name'] == classroom_name) &
                ((schedules_df['start_time'] < end_dt) & (schedules_df['end_time'] > start_dt))
            ]

            if not overlapping.empty:
                messagebox.showerror("Error", "Scheduling conflict detected!")
                return

            new_booking = pd.DataFrame([{
                "classroom_name": classroom_name,
                "start_time": start_date,
                "end_time": end_date,
                "reserved_by": reserved_by,
                "purpose": purpose
            }])
            schedules_df = pd.concat([schedules_df, new_booking], ignore_index=True)
            save_df_to_db('classroom_schedules', schedules_df,0)

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

            selected_events = schedules_df[schedules_df['start_date'] == selected_date_obj]
            self.events_list.delete(0, tk.END)

            for _, event in selected_events.iterrows():
                event_info = f"{event['classroom_name']} | {event['start_time']} - {event['end_time']} | Purpose: {event['purpose']}"
                self.events_list.insert(tk.END, event_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show events: {e}")
