import customtkinter
import sys
import os
from tkinter import ttk, messagebox
import sqlite3

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER | Add Guests")  # Title of the form
        self.geometry("360x370")  # Dimensions of the form

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

        # Label for event type
        self.lbl_event = customtkinter.CTkLabel(self.form_frame_content, text="Select Hosts:")
        self.lbl_event.grid(row=1, column=0, pady=(10, 0), padx=(0, 220))

        # Input | Event Type (Combo Box)
        self.entry_host_id = customtkinter.CTkComboBox(self.form_frame_content, corner_radius=20, width=300, fg_color="white", text_color='black', command=self.populate_guest_info)
        self.entry_host_id.grid(row=2, column=0, pady=5, padx=10)
        self.load_client_ids()  # Load client IDs into the combo box

        # Input | Guest Name
        self.guest_name_entry = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Name", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.guest_name_entry.grid(row=3, column=0, pady=5, padx=10)

        # Input | Guest Email 
        self.guest_email_entry = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Email", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.guest_email_entry.grid(row=4, column=0, pady=5, padx=10)
        
        # Label for category
        self.lbl_event = customtkinter.CTkLabel(self.form_frame_content, text="Event Type:")
        self.lbl_event.grid(row=5, column=0, pady=(10, 0), padx=(0, 220))

        # Input | Event Type (Combo Box)
        self.entry_event_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding", "Birthday Party", "Conference", "Gender Reveals", "Graduation", "Funerals"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_event_type.grid(row=6, column=0, pady=5, padx=10)

        addGuest_btn = customtkinter.CTkButton(self.form_frame_content, text="Add Guest", command=self.handle_guest_submission)
        addGuest_btn.grid(row=7, column=0, columnspan=2, pady=10)

    def load_client_ids(self):
        """Load client IDs from the events table into the combo box."""
        try:
            with sqlite3.connect("events.db") as conn:
                c = conn.cursor()
                c.execute("SELECT client_id FROM events")
                client_ids = c.fetchall()
                # Check if client_ids is empty
                if not client_ids:
                    self.entry_host_id.configure(values=[], state="disabled")  # Disable if no IDs found
                else:
                    self.entry_host_id.configure(values=[str(client_id[0]) for client_id in client_ids])  # Populate the combo box
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading client IDs: {e}")

    def populate_guest_info(self, selected_client_id):
        """Populate guest name and email fields based on selected client ID."""
        if selected_client_id:
            with sqlite3.connect("events.db") as conn:
                c = conn.cursor()
                c.execute("SELECT client_name, client_email FROM events WHERE client_id = ?", (selected_client_id,))
                result = c.fetchone()
                if result:
                    client_name, client_email = result
                    self.guest_name_entry.delete(0, 'end')  # Clear previous entry
                    self.guest_name_entry.insert(0, client_name)  # Populate guest name
                    self.guest_email_entry.delete(0, 'end')  # Clear previous entry
                    self.guest_email_entry.insert(0, client_email)  # Populate guest email

    def handle_guest_submission(self):
        name = self.guest_name_entry.get()
        email = self.guest_email_entry.get()
        host_id = self.entry_host_id.get()
        guest_event = self.entry_event_type.get()
        if name and email and host_id:
            # Retrieve client name and email based on selected client_id
            client_name, client_email = self.get_client_info(host_id)
            if client_name and client_email:
                self.add_guest_to_event(name, email, host_id, guest_event, client_name, client_email)
            else:
                messagebox.showwarning("Input Error", "Client information could not be retrieved.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            
    def get_client_info(self, client_id):
        """Retrieve client name and email based on client_id."""
        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            c.execute("SELECT client_name, client_email FROM events WHERE client_id = ?", (client_id,))
            result = c.fetchone()
            if result:
                return result  # Returns (client_name, client_email)
        return None, None  # Return None if no result found


    # Function to add guest to the event
    def add_guest_to_event(self, name, email, client_id, guest_event, client_name, client_email):
        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute("INSERT INTO guests (event_title, name, email, client_id, client_name, client_email) VALUES (?, ?, ?, ?, ?, ?)", 
                (guest_event, name, email, client_id, client_name, client_email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Guest '{name}' added to event ID: '{client_id}'!")

if __name__ == "__main__":
    app = App()
    app.mainloop()