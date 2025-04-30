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
        self.title("Event Planner | Modify Events")  # Title of the form
        self.geometry("370x500")  # dimensions of the form

        # Main content area
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame, border_width=1)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        # Call the function to create the form and image
        self.show_event_form()

    def show_event_form(self, client_id="", title="", date="", time="", location="", category="", client_name="", description=""):
        self.clear_content()

        title_label = customtkinter.CTkLabel(self.form_frame_content, text="Modify Events", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input | client Id
        self.entry_client_id = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="client ID", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_client_id.grid(row=1, column=1, pady=5, padx=10)
        self.entry_client_id.insert(0, client_id)  # Populate with existing title

        # Input | Title
        self.entry_title = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Title", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_title.grid(row=2, column=1, pady=5, padx=10)
        self.entry_title.insert(0, title)  # Populate with existing title

        # Input | Date
        self.entry_date = tkcalendar.DateEntry(self.form_frame_content, width=45, background='2b2b2b',
                                        foreground='white', borderwidth=1, date_pattern='y-mm-dd')
        self.entry_date.grid(row=3, column=1, pady=5, padx=10)

        # Check if the date is valid before setting it
        if date:
            try:
                # Assuming date is in 'YYYY-MM-DD' format, convert it to a date object
                year, month, day = map(int, date.split('-'))
                self.entry_date.set_date(datetime.date(year, month, day))  # Set the date
            except ValueError:
                messagebox.showerror("Date Error", f"Invalid date format: {date}")

        # Input | Time
        self.entry_time = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Time", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_time.grid(row=4, column=1, pady=5, padx=10)
        self.entry_time.insert(0, time)  # Populate with existing time

        # Input | Location
        self.entry_location = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Location", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.entry_location.grid(row=5, column=1, pady=5, padx=10)
        self.entry_location.insert(0, location)  # Populate with existing location

        # Input | Event Type (Combo Box)
        self.entry_event_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding", "Birthday Party", "Conference", "Gender Reveals", "Graduation", "Funerals"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_event_type.grid(row=6, column=1, pady=5, padx=10)
        self.entry_event_type.set(category)  # Populate with existing category

        # Input | Client Name
        self.entry_client_name = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Client Name", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.entry_client_name.grid(row=7, column=1, pady=5, padx=10)
        self.entry_client_name.insert(0, client_name)  # Populate with existing location

        # Input | Description
        self.text_description = customtkinter.CTkTextbox(self.form_frame_content, fg_color="white", height=80, width=300 , text_color='black')
        self.text_description.grid(row=8, column=1, pady=5, padx=10)
        self.text_description.insert("1.0", description)  # Populate with existing description

        # Button frame
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=10)

        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Event", command=lambda: self.delete_event(title, client_id))
        delete_btn.grid(row=0, column=0, pady=10, padx=20)

        update_btn = customtkinter.CTkButton(btn_frame, text="Update Event", command=self.update_event)
        update_btn.grid(row=0, column=1, pady=10)

    def delete_event(self, title, client_id):
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete the event '{title}'?")
        if confirm:
            conn = sqlite3.connect("events.db")
            c = conn.cursor()
            c.execute("DELETE FROM events WHERE clent_id=?", (client_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Event deleted successfully!")
            self.close_event_form()  # Close the modify events form
            from eventplanner_section import App as planner
            planner().show_saved_events()  # Refresh the events list in the main app

    def update_event(self):
        updated_client_id = self.entry_client_id.get()
        updated_title = self.entry_title.get()
        updated_date = self.entry_date.get()
        updated_time = self.entry_time.get()
        updated_location = self.entry_location.get()
        updated_category = self.entry_location.get()
        updated_client_name = self.entry_client_name.get()
        updated_description = self.text_description.get("1.0", "end-1c")

        if not all([updated_title, updated_date, updated_time, updated_location, updated_category, updated_client_name, updated_description]):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute("UPDATE events SET title=?, date=?, time=?, location=?, category=?, client_name=? description=? WHERE client_id=?", 
                  (updated_title, updated_date, updated_time, updated_location, updated_category, updated_client_name, updated_description, updated_client_id))
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