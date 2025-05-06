import customtkinter
import sys
import os
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
import sqlite3
import datetime
import tkcalendar  # Import DateEntry from tkcalendar

sys.path.append(os.path.abspath("C:\\Users\\Emmanual.Januarie\\Documents\\GitHub\\tkinter-event-planner"))

customtkinter.set_appearance_mode("dark")  # Set dark mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("Event Planner | Modify Guest")  # Title of the form
        self.geometry("370x500")  # dimensions of the form

        # Main content area
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame, border_width=1)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        # Call the function to create the form and image
        self.show_guest_form()

    
    def show_guest_form(self, client_id="", category="", name="", email=""):
        self.clear_content()

        title_label = customtkinter.CTkLabel(self.form_frame_content, text="Modify Events", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input | client Id
        self.entry_client_id = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="client ID", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_client_id.grid(row=1, column=1, pady=5, padx=10)
        self.entry_client_id.insert(0, client_id)  # Populate with existing title

        # Input | Event Type (Combo Box)
        self.entry_event_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding", "Birthday Party", "Conference", "Gender Reveals", "Graduation", "Funerals"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_event_type.grid(row=2, column=1, pady=5, padx=10)
        self.entry_event_type.set(category)  # Populate with existing category

         # Input | Event Type (Combo Box)
        self.entry_clientid_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["1", "2", "3", "4", "5", "6"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_clientid_type.grid(row=3, column=1, pady=5, padx=10)
        self.entry_clientid_type.set(category)  # Populate with existing category

        # Input | Guest Name
        self.entry_guest_name = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Name", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.entry_guest_name.grid(row=4, column=1, pady=5, padx=10)
        self.entry_guest_name.insert(0, name)  # Populate with existing location

        # Input | Guest Email
        self.entry_guest_email = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Guest Email", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.entry_guest_email.grid(row=5, column=1, pady=5, padx=10)
        self.entry_guest_email.insert(0, email)  # Populate with existing location

        # Button frame
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Guest", command=lambda: self.delete_event(client_id))
        delete_btn.grid(row=0, column=0, pady=10, padx=20)

        update_btn = customtkinter.CTkButton(btn_frame, text="Update Guest", command=self.update_event)
        update_btn.grid(row=0, column=1, pady=10)

        
    def delete_event(self, client_id):
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete the guest with ID: '{client_id}'?")
        if confirm:
            conn = sqlite3.connect("events.db")
            c = conn.cursor()
            
            # Wrap client_id in a tuple
            c.execute("DELETE FROM events WHERE client_id=?", (client_id,))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Event deleted successfully!")
            self.close_event_form()  # Close the modify events form
            
            # Refresh the events list in the main app
            from eventplanner_section import App as planner
            planner().show_saved_events()

    def update_event(self):
        updated_client_id = self.entry_client_id.get()
        updated_date = self.entry_date.get()
        updated_time = self.entry_time.get()
        updated_location = self.entry_location.get()
        updated_category = self.entry_location.get()
        updated_client_name = self.entry_client_name.get()
        updated_description = self.text_description.get("1.0", "end-1c")

        if not all([updated_date, updated_time, updated_location, updated_category, updated_client_name, updated_description]):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute("UPDATE events SET category=?, date=?, time=?, location=?, client_name=?,  description=? WHERE client_id=?", 
                  (updated_category, updated_date, updated_time, updated_location, updated_client_name, updated_description, updated_client_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Event updated successfully!")
        self.close_event_form()  # Close the modify events form

    def clear_content(self):
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()

    def close_event_form(self):
        self.destroy()  # Close the modify events form

if __name__ == "__main__":
    app = App()
    app.mainloop()