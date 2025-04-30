import customtkinter
from tkinter import ttk, messagebox
import sqlite3

# Set the appearance mode to dark and the default color theme to blue
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Database setup function to initialize the SQLite database
def init_db():
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    # Create the events table if it doesn't already exist
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    title TEXT,
                    date TEXT,
                    time TEXT,
                    location TEXT,
                    description TEXT)''')
    conn.commit()  # Commit the changes to the database
    conn.close()   # Close the database connection

# Main application class for the Event Planner
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.title("EVENT PLANNER")  # Set the window title
        self.geometry("1090x519")  # Set the window size

        init_db()  # Initialize the database
        self.create_event_planner_GUI()  # Create the GUI for the event planner

    '''Function to log out the user and switch to the login GUI'''
    def logout_User(self):
        from login import App as LoginGUI  # Import the login GUI
        self.destroy()  # Remove the current GUI
        self.loginGUI = LoginGUI()  # Create an instance of the login GUI
        self.loginGUI.mainloop()  # Run the login GUI

    '''Function to toggle the Create Event Form'''
    def toggle_createEventForm(self):
        from createEvent import App as CreateEventGui  # Import the Create Event GUI
        self.CreateEventGui = CreateEventGui()  # Create an instance of the Create Event GUI
        self.CreateEventGui.mainloop()  # Run the Create Event GUI

    '''Function to toggle the Create Quote Form'''
    def toggle_createQuoteForm(self):
        from createQuote import App as CreateQuoteGUI  # Import the Create Quote GUI
        self.CreateQuoteGUI = CreateQuoteGUI()  # Create an instance of the Create Quote GUI
        self.CreateQuoteGUI.mainloop()  # Run the Create Quote GUI

    '''Function to create the main GUI layout for the event planner'''
    def create_event_planner_GUI(self):
        # Create a sidebar frame for navigation
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Add a label to the sidebar
        self.label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # Add buttons to the sidebar for different functionalities
        self.dashboard_btn = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", fg_color="#2b2b2b", hover_color="gray",
                                                     command=self.show_dashboard)
        self.dashboard_btn.pack(pady=10)

        self.events_btn = customtkinter.CTkButton(self.sidebar_frame, text="Events", fg_color="#2b2b2b", hover_color="gray", 
                                                  command=self.show_saved_events)
        self.events_btn.pack(pady=10)

        self.another_btn = customtkinter.CTkButton(self.sidebar_frame, text="Another", fg_color="#2b2b2b", hover_color="gray",
                                                   command=self.show_placeholder)
        self.another_btn.pack(pady=10)

        # Configure the sidebar frame
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack_configure()
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.pack_configure()

        # Logout button at the bottom of the sidebar
        self.logout_btn = customtkinter.CTkButton(self.sidebar_frame, text="Logout", command=self.logout_User)
        self.logout_btn.pack(side="bottom", pady=20)

        # Main content area for displaying forms and information
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        self.show_dashboard()  # Display the dashboard by default when the app starts

    '''Function to clear the content of the main form frame'''
    def clear_content(self):
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()  # Remove all widgets from the content area

    '''Function to display the dashboard view'''
    def show_dashboard(self):
        self.clear_content()  # Clear previous content
        self.title("Event Planner | Dashboard")  # Update window title
        title = customtkinter.CTkLabel(self.form_frame_content, text="Dashboard", font=("Arial", 18, "bold"))
        title.pack(pady=20)  # Add title label to the dashboard

    '''Function to display saved events in a list'''
    def show_saved_events(self):
        self.clear_content()  # Clear previous content
        self.title("Event Planner | Events")  # Update window title

        # Search input for filtering events
        self.search_input = customtkinter.CTkEntry(self.form_frame_content, placeholder_text="Search...", corner_radius=20,
                                                  width=800, border_width=1, fg_color="white", text_color="black")
        self.search_input.pack(padx=10, pady=10)  # Add search input to the form

        # Frame for the events table
        table_frame = customtkinter.CTkFrame(self.form_frame_content, width=0)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview for displaying events
        self.tree = ttk.Treeview(table_frame, columns=("Title", "Date", "Time", "Location", "Description"), show="headings")
        for col in ("Title", "Date", "Time", "Location", "Description"):
            self.tree.heading(col, text=col)  # Set column headings
            self.tree.column(col, width=150 if col in ["Title", "Location"] else 100)  # Set column widths

        self.tree.pack(fill="both", expand=True)  # Add the treeview to the table frame
        self.load_events_into_tree()  # Load events from the database into the treeview

        # Bind the selection event to update the selected event
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.update_selected_event())

        # Frame for action buttons
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.pack(pady=10)

        # Button to create a quote
        update_btn = customtkinter.CTkButton(btn_frame, text="Create Quote", command=self.toggle_createQuoteForm)
        update_btn.grid(row=0, column=0, padx=10)

        # Button to create a new event
        delete_btn = customtkinter.CTkButton(btn_frame, text="Create Event", command=self.toggle_createEventForm)
        delete_btn.grid(row=0, column=1, padx=10)

    '''Function to load events from the database into the treeview'''
    def load_events_into_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear existing rows in the treeview

        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM events")  # Query to select all events
            events = c.fetchall()  # Fetch all events

        for event in events:
            self.tree.insert("", "end", values=event)  # Insert each event into the treeview

    '''Function to update the selected event in the treeview'''
    def update_selected_event(self):
        selected_item = self.tree.focus()  # Get the currently selected item
        if not selected_item:
            messagebox.showwarning("Select Event", "Please select an event to update.")  # Show warning if no event is selected
            return

        data = self.tree.item(selected_item)["values"]  # Get the values of the selected event
        if data:
            from modifyEventsForm import App as modifyEvents  # Import the modify events GUI
            modifyEvents_instance = modifyEvents()  # Create an instance of the modify events GUI
            modifyEvents_instance.show_event_form(
                title=data[0],
                date=data[1],
                time=data[2],
                location=data[3],
                description=data[4]  # Pass the event details to the modify events form
            )
            modifyEvents_instance.mainloop()  # Run the modify events GUI

    '''Function to delete the selected event from the treeview'''
    def delete_selected_event(self):
        selected_item = self.tree.focus()  # Get the currently selected item
        if not selected_item:
            messagebox.showwarning("Select Event", "Please select an event to delete.")  # Show warning if no event is selected
            return

        data = self.tree.item(selected_item)["values"]  # Get the values of the selected event
        confirm = messagebox.askyesno("Delete", f"Delete event '{data[0]}'?")  # Confirm deletion
        if confirm:
            conn = sqlite3.connect("events.db")  # Connect to the database
            c = conn.cursor()
            c.execute("DELETE FROM events WHERE title=? AND date=? AND time=?", (data[0], data[1], data[2]))  # Delete the event
            conn.commit()  # Commit the changes
            conn.close()  # Close the database connection
            messagebox.showinfo("Deleted", "Event deleted successfully!")  # Show success message
            self.load_events_into_tree()  # Reload events into the treeview

    '''Function to show a placeholder view'''
    def show_placeholder(self):
        self.clear_content()  # Clear previous content
        label = customtkinter.CTkLabel(self.form_frame_content, text="Another View Placeholder", font=("Arial", 18))  # Placeholder label
        label.pack(pady=20)  # Add placeholder label to the content area

# Main entry point of the application
if __name__ == "__main__":
    app = App()  # Create an instance of the App class
    app.mainloop()  # Run the application loop