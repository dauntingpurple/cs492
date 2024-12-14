import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
from datetime import datetime


class CommunicationSystem:
    def __init__(self, parent, current_user):
        """
        Initializes the Communication System.

        Args:
            parent (tk.Widget): The parent Tkinter frame for embedding into a tab.
            current_user (str): The current user (role or username).
        """
        self.parent = parent
        self.current_user = current_user  # Store the current user's role or name

        # Initialize a DataFrame to store messages
        self.messages_df = pd.DataFrame(columns=['sender', 'receiver', 'message_text', 'timestamp', 'is_read'])
        self.unsent_messages = []  # Temporary storage for unsent messages

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI for messaging.
        """
        tk.Label(self.parent, text=f"Logged in as: {self.current_user}", font=("Arial", 12, "bold")).pack(pady=5)

        # Receiver
        tk.Label(self.parent, text="Receiver:").pack()
        self.receiver_entry = tk.Entry(self.parent)
        self.receiver_entry.pack()

        # Message Text
        tk.Label(self.parent, text="Message:").pack()
        self.message_text_entry = scrolledtext.ScrolledText(self.parent, width=40, height=10)
        self.message_text_entry.pack()

        # Send Message Button
        tk.Button(self.parent, text="Send Message", command=self.send_message).pack(pady=5)

        # Message List
        tk.Label(self.parent, text="Messages:").pack()
        self.message_list = scrolledtext.ScrolledText(self.parent, width=50, height=15)
        self.message_list.pack()

        self.load_messages()  # Load initial messages

    def send_message(self):
        """
        Handles sending messages.
        """
        sender = self.current_user
        receiver = self.receiver_entry.get()
        message_text = self.message_text_entry.get("1.0", tk.END).strip()

        if not receiver or not message_text:
            messagebox.showwarning("Warning", "Receiver and message text are required!")
            return

        # Create a new message entry
        new_message = {
            'sender': sender,
            'receiver': receiver,
            'message_text': message_text,
            'timestamp': datetime.now(),
            'is_read': False
        }

        # Convert new_message to a DataFrame
        new_message_df = pd.DataFrame([new_message])

        # Append new_message_df to the main DataFrame
        if self.messages_df.empty:
            self.messages_df = new_message_df
        else:
            self.messages_df = pd.concat([self.messages_df, new_message_df], ignore_index=True)

        # Clear the message text box
        self.message_text_entry.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Message sent successfully!")
        self.load_messages()

    def load_messages(self):
        """
        Loads and displays messages relevant to the current user.
        """
        self.message_list.delete(1.0, tk.END)  # Clear current messages

        # Filter messages for the current user
        user_messages = self.messages_df[
            (self.messages_df['sender'] == self.current_user) |
            (self.messages_df['receiver'] == self.current_user)
        ]

        for _, msg in user_messages.iterrows():
            msg_display = f"{msg['sender']} to {msg['receiver']}: {msg['message_text']} (at {msg['timestamp']})\n"
            self.message_list.insert(tk.END, msg_display)


if __name__ == "__main__":
    # Example standalone usage; replace with dynamic integration in main application
    root = tk.Tk()
    root.title("Messaging System")
    root.geometry("500x600")
    CommunicationSystem(root, current_user="Admin")
    root.mainloop()
