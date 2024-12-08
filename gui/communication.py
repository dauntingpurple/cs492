import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
from datetime import datetime

#need to get how the user to and from somehow
class CommunicationSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Teacher-Administrator Communication")

        # Initialize a DataFrame to store messages
        self.messages_df = pd.DataFrame(columns=['sender', 'receiver', 'message_text', 'timestamp', 'is_read'])
        self.unsent_messages = []  # Temporary storage for unsent messages

        # GUI Elements
        self.setup_gui()

    def run(self):
        """
        Starts the GUI application.
        """
        # Sender
        tk.Label(self.master, text="Sender:").pack()
        self.sender_entry = tk.Entry(self.master)
        self.sender_entry.pack()

        # Receiver
        tk.Label(self.master, text="Receiver:").pack()
        self.receiver_entry = tk.Entry(self.master)
        self.receiver_entry.pack()

        # Message Text
        tk.Label(self.master, text="Message:").pack()
        self.message_text_entry = scrolledtext.ScrolledText(self.master, width=40, height=10)
        self.message_text_entry.pack()

        # Send Message Button
        send_button = tk.Button(self.master, text="Send Message", command=self.send_message)
        send_button.pack()

        # Message List
        tk.Label(self.master, text="Messages:").pack()
        self.message_list = scrolledtext.ScrolledText(self.master, width=50, height=15)
        self.message_list.pack()

    def send_message(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        message_text = self.message_text_entry.get("1.0", tk.END).strip()

        if not sender or not receiver or not message_text:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        # Create a new message entry
        new_message = {
            'sender': sender,
            'receiver': receiver,
            'message_text': message_text,
            'timestamp': datetime.now(),
            'is_read': False
        }

        # Append the new message to the temporary storage
        self.unsent_messages.append(new_message)

        # Move unsent messages to the main DataFrame
        self.messages_df = self.messages_df.append(new_message, ignore_index=True)

        self.message_text_entry.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Message sent successfully!")
        self.load_messages()

    def load_messages(self):
        self.message_list.delete(1.0, tk.END)  # Clear current messages
        # Filter messages for the current user (both as sender and receiver)
        user_messages = self.messages_df[
            (self.messages_df['sender'] == self.current_user) |
            (self.messages_df['receiver'] == self.current_user)
        ]

        for _, msg in user_messages.iterrows():
            msg_display = f"{msg['sender']} to {msg['receiver']}: {msg['message_text']} (at {msg['timestamp']})\n"
            self.message_list.insert(tk.END, msg_display)

if __name__ == "__main__":
    root = tk.Tk()
    communication_system = CommunicationSystem(root)
    root.mainloop()