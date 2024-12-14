import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
from datetime import datetime
from src.saveChangeToDatabase import save_df_to_db, read_from_df


class CommunicationSystem:
    def __init__(self, master, current_user):
        """
        Initializes the Communication System.

        Args:
            master (tk.Toplevel): The parent Tkinter window.
            current_user (str): The current user (role or username).
        """
        self.master = master
        self.master.title("Teacher-Administrator Communication")
        self.current_user = current_user  # Store the current user's role or name

        # Initialize a DataFrame to store messages
        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI for messaging.
        """
        tk.Label(self.master, text=f"Logged in as: {self.current_user}", font=("Arial", 12, "bold")).pack(pady=5)

        # Receiver
        tk.Label(self.master, text="Receiver:").pack()
        self.receiver_entry = tk.Entry(self.master)
        self.receiver_entry.pack()

        # Message Text
        tk.Label(self.master, text="Message:").pack()
        self.message_text_entry = scrolledtext.ScrolledText(self.master, width=40, height=10)
        self.message_text_entry.pack()

        # Send Message Button
        tk.Button(self.master, text="Send Message", command=self.send_message).pack(pady=5)

        # Message List
        tk.Label(self.master, text="Messages:").pack()
        self.message_list = scrolledtext.ScrolledText(self.master, width=50, height=15)
        self.message_list.pack()

        self.load_messages()  # Load initial messages

    def send_message(self):
        """
        Handles sending messages.
        """
        sender = self.current_user
        receiver = self.receiver_entry.get()
        message_text = self.message_text_entry.get("1.0", tk.END).strip()

        messages_df = read_from_df('messages')


        if not receiver or not message_text:
            messagebox.showwarning("Warning", "Receiver and message text are required!")
            return

        # Create a new message entry
        new_message = pd.DataFrame({
            'sender': sender,
            'receiver': receiver,
            'message_text': message_text,
            'timestamp': datetime.now(),
            'is_read': False
        })

        # Append new_message_df to the main DataFrame
        if messages_df.empty:
            messages_df = new_message
        else:
            messages_df = pd.concat([messages_df, new_message], ignore_index=True)
            save_df_to_db('messages', messages_df)
            
        # Clear the message text box
        self.message_text_entry.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Message sent successfully!")
        self.load_messages()

    def load_messages(self):
        """
        Loads and displays messages relevant to the current user.
        """
        self.message_list.delete(1.0, tk.END)  # Clear current messages
        messages_df = read_from_df('messages')

        # Filter messages for the current user
        user_messages = messages_df[
            (messages_df['sender'] == self.current_user) |
            (messages_df['receiver'] == self.current_user)
        ]

        for _, msg in user_messages.iterrows():
            msg_display = f"{msg['sender']} to {msg['receiver']}: {msg['message_text']} (at {msg['timestamp']})\n"
            self.message_list.insert(tk.END, msg_display)


if __name__ == "__main__":
    root = tk.Tk()
    current_user = "Admin"  # Example user; replace with dynamic user role
    communication_system = CommunicationSystem(root, current_user)
    root.mainloop()
