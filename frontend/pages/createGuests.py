import customtkinter
import sys
import os
from tkinter import ttk, messagebox
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image, ImageTk, ImageDraw
import sqlite3
sys.path.append(os.path.abspath("C:\\Users\\tallyta\\Documents\\GitHub\\tkinter-event-planner"))

#Importing registration GUI
from registration import App as RegistrationGUI

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER | Add Guests") #Title of the form
        self.geometry("690x270") #dimensions of the form

        # Main content area
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame, border_width=1)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        self.show_guest_form()

    def clear_content(self):
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()

    

    # Call the function to create the form and image
    def show_guest_form(self):
        self.clear_content()
        self.title("Event Planner | Add Guest")

        title = customtkinter.CTkLabel(self.form_frame_content, text="Add Guests", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input | Event Type (Combo Box)
        self.entry_guest_id = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding", "Birthday Party", "Conference", "Gender Reveals", "Graduation", "Funerals"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_guest_id.grid(row=1, column=0, pady=5, padx=10)

        # Input | Guest Name
        self.guest_name_entry = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Name", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.guest_name_entry.grid(row=2, column =0, pady=5, padx=10)

        # Input | Guest Email 
        self.guest_email_entry = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Email", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.guest_email_entry.grid(row=3, column =0, pady=5, padx=10)
    

        addGuest_btn = customtkinter.CTkButton(self.form_frame_content, text="Add Guest", command=self.handle_guest_submission)
        addGuest_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Function to handle guest submission
    def handle_guest_submission(self):
        name = self.guest_name_entry.get()
        email = self.guest_email_entry.get()
        guest_id = self.entry_guest_id.get()

        if name and email and guest_id:
            self.add_guest_to_event(name, email, guest_id)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    # Function to add guest to the event

    def add_guest_to_event(self, name, email, client_id):
        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute("INSERT INTO guests (client_id, name, email) VALUES (?, ?, ?)", (client_id, name, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Guest '{name}' added to event ID: '{client_id}'!")

    # Function to view guests
    def view_guests_for_selected_event(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select an event first.")
            return

        event_data = self.tree.item(selected_item)["values"]
        if not event_data:
            messagebox.showwarning("No data", "Could not read event data.")
            return

        event_title = event_data[0]

        guests_window = customtkinter.CTkToplevel(self)
        guests_window.title(f"Guests for {event_title}")
        guests_window.geometry("500x400")
        guests_window.lift()
        guests_window.attributes("-topmost", True)
        guests_window.after(1, lambda: guests_window.attributes("-topmost", False))

        customtkinter.CTkLabel(guests_window, text=f"Guests for: {event_title}", font=("Arial", 16, "bold")).pack(pady=10)

        guest_tree = ttk.Treeview(guests_window, columns=("Name", "Email"), show="headings")
        guest_tree.heading("Name", text="Name")
        guest_tree.heading("Email", text="Email")
        guest_tree.column("Name", width=200)
        guest_tree.column("Email", width=250)
        guest_tree.pack(padx=10, pady=10, fill="both", expand=True)

        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            c.execute("SELECT name, email FROM guests WHERE event_title = ?", (event_title,))
            guests = c.fetchall()

        if guests:
            for guest in guests:
                guest_tree.insert("", "end", values=guest)
        else:
            messagebox.showinfo("No Guests", f"No guests found for event '{event_title}'.")




if __name__ == "__main__":
    app = App()
    app.mainloop()