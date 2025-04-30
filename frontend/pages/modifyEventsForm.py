import customtkinter
import sys
import os
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
import sqlite3
import tkcalendar  # Import DateEntry from tkcalendar

sys.path.append(os.path.abspath("C:\\Users\\Emmanual.Januarie\\Documents\\GitHub\\tkinter-event-planner"))

customtkinter.set_appearance_mode("dark")  # Set dark mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("Event Planner | Modify Events")  # Title of the form
        self.geometry("370x460")  # dimensions of the form

        # Main content area
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame, border_width=1)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        # Call the function to create the form and image
        self.show_event_form()

    def clear_content(self):
        # Clear the content of the form
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()

    def create_event_form(self):
        title = self.entry_title.get()
        date = self.entry_date.get()
        time = self.entry_time.get()
        location = self.entry_location.get()
        category = self.entry_event_type.get()
        description = self.text_description.get("1.0", "end").strip()

        if not all([title, date, time, location, category, description]):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        conn = sqlite3.connect("events.db")
        c = conn.cursor()
        c.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", (title, date, time, location, category, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Event added successfully!")

        self.entry_title.delete(0, 'end')
        self.entry_date.delete('')
        self.entry_time.delete(0, 'end')
        self.entry_location.delete(0, 'end')
        self.entry_event_type.delete('')
        self.text_description.delete("1.0", "end")

        # Direct user back to event planner
        from eventplanner_section import App as planner
        planner.show_saved_events()

    def show_event_form(self, title="", date="", time="", location="", category="", description=""):
        self.clear_content()

        title_label = customtkinter.CTkLabel(self.form_frame_content, text="Modify Events", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input | Title
        self.entry_title = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Title", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_title.grid(row=1, column=1, pady=5, padx=10)
        self.entry_title.insert(0, title)  # Populate with existing title

        # Input | Date
        self.entry_date = tkcalendar.DateEntry(self.form_frame_content, width=45, background='2b2b2b',
                                     foreground='white', borderwidth=1, date_pattern='y-mm-dd')
        self.entry_date.grid(row=2, column=1, pady=5, padx=10)

        # Input | Time
        self.entry_time = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Time", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_time.grid(row=3, column=1, pady=5, padx=10)
        self.entry_time.insert(0, time)  # Populate with existing time

        # Input | Location
        self.entry_location = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Location", corner_radius=20,
                                                      width=300, border_width=0, text_color='black')
        self.entry_location.grid(row=4, column=1, pady=5, padx=10)
        self.entry_location.insert(0, location)  # Populate with existing location

        # Input | Event Type (Combo Box)
        self.entry_event_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding", "Birthday Party", "Conference", "Gender Reveals", "Graduation", "Funerals"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_event_type.grid(row=5, column=1, pady=5, padx=10)

        # Input | Description
        self.text_description = customtkinter.CTkTextbox(self.form_frame_content, fg_color="white", height=80, width=300, text_color='black')
        self.text_description.grid(row=6, column=1, pady=5, padx=10)

        # Button frame
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        delete_btn = customtkinter.CTkButton(btn_frame, text="Delete Event")
        delete_btn.grid(row=0, column=0, pady=10, padx=20)

        update_btn = customtkinter.CTkButton(btn_frame, text="Update Event")
        update_btn.grid(row=0, column=1, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()