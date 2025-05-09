import customtkinter
from tkinter import ttk, messagebox
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt

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
                    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    date TEXT,
                    time TEXT,
                    location TEXT,
                    client_name TEXT,
                    client_email TEXT,
                    description TEXT)''')
    
    # Create the guests table if it doesn't already exist
    c.execute('''CREATE TABLE IF NOT EXISTS guests (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_title TEXT,
                    name TEXT, 
                    email TEXT,
                    client_id INTEGER,
                    client_name TEXT,
                    client_email TEXT,
                    FOREIGN KEY (client_id) REFERENCES events(client_id))''')
    
    #function to create total_of_sales database
    c.execute('''
            CREATE TABLE IF NOT EXISTS total_of_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_email TEXT NOT NULL,
                food_type TEXT NOT NULL,
                sides TEXT NOT NULL,
                beverages TEXT NOT NULL,
                guest_count INTEGER NOT NULL,
                total_price REAL NOT NULL
            )
        ''')
    
    conn.commit()  # Commit the changes to the database
    conn.close()   # Close the database connection
    
# Main application class for the Event Planner
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.debounce_timer = None  # Timer for debounce
        
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

    '''Function to toggle the create guest form'''
    def toggle_createGuestForm(self):
        from createGuests import App as CreateGuestGUI  # Import the Create Quote GUI
        self.CreateGuestGUI = CreateGuestGUI()  # Create an instance of the Create Quote GUI
        self.CreateGuestGUI.mainloop()  # Run the Create Quote GUI



    '''Function to create the main GUI layout for the event planner'''
    def create_event_planner_GUI(self):
        # Create a sidebar frame for navigation
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Add a label to the sidebar
        self.label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # Add buttons to the sidebar for different functionalities
        self.dashboard_btn = customtkinter.CTkButton(self.sidebar_frame, text="Home", fg_color="#2b2b2b", hover_color="gray",
                                                     command=self.show_home)
        self.dashboard_btn.pack(pady=10)

        self.dashboard_btn = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", fg_color="#2b2b2b", hover_color="gray",
                                                     command=self.show_dashboard)
        self.dashboard_btn.pack(pady=10)

        self.events_btn = customtkinter.CTkButton(self.sidebar_frame, text="Events", fg_color="#2b2b2b", hover_color="gray", 
                                                  command=self.show_saved_events)
        self.events_btn.pack(pady=10)

        self.another_btn = customtkinter.CTkButton(self.sidebar_frame, text="Guests", fg_color="#2b2b2b", hover_color="gray",
                                                   command=self.show_saved_guests)
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

        self.show_home()  # Display the dashboard by default when the app starts

    '''Function to clear the content of the main form frame'''
    def clear_content(self):
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()  # Remove all widgets from the content area
    
    def show_home(self):
        self.clear_content()
        self.title("Event Planner | Home")
 
        # Load and display background image
        bg_image = Image.open("frontend/src/assests/event.jpg")
        bg_image = bg_image.resize((850, 400), Image.LANCZOS)
 
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = customtkinter.CTkLabel(self.form_frame_content, image=self.bg_image_tk, text="")
        bg_label.pack(fill="both", expand=True, padx=20, pady=20)
 
        # Transparent text overlays
        title = customtkinter.CTkLabel(self.form_frame_content, text="", font=("Arial", 30, "bold"), text_color="white")
        title.place(relx=0.5, rely=0.2, anchor="center")
       
        subtitle = customtkinter.CTkLabel(self.form_frame_content, text="Plan. Organize. Celebrate.", font=("Arial", 30, "italic"),                      text_color="white")
        subtitle.place(relx=0.5, rely=0.3, anchor="center")
       
        info = customtkinter.CTkLabel(self.form_frame_content, text="Effortlessly manage your events, guests, and quotes all in one place.\n\nStart creating unforgettable moments today.", font=("Arial", 18), text_color="blue")

    '''Function to display the dashboard view'''
    def show_dashboard(self):
        self.clear_content()  # Clear previous content
        self.title("Event Planner | Dashboard")  # Update window title

        dashboard_container = customtkinter.CTkFrame(self.form_frame_content)
        dashboard_container.pack(padx=2, pady=2, fill="both", expand=True)

        # Create vertical container to hold top charts, bottom line chart, and triple charts row
        charts_vertical_container = customtkinter.CTkFrame(dashboard_container, fg_color="#2b2b2b")
        charts_vertical_container.pack(fill="both", expand=True)

        # Top horizontal frame for bar and pie charts (2 charts)
        top_charts_frame = customtkinter.CTkFrame(charts_vertical_container)
        top_charts_frame.pack(side="top", fill="both", expand=True)

        # Bar Chart Frame (left)
        bar_chart_frame = customtkinter.CTkFrame(top_charts_frame,
                                                corner_radius=25, border_width=0)
        bar_chart_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Pie Chart Frame (right)
        pie_chart_frame = customtkinter.CTkFrame(top_charts_frame,
                                                corner_radius=25, border_width=0)
        pie_chart_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Bottom frame for line chart (total sales over time)
        bottom_chart_frame = customtkinter.CTkFrame(charts_vertical_container,
                                                    corner_radius=25, border_width=0, fg_color="#333333")
        bottom_chart_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Frame for three charts row (food_type, sides, beverages)
        triple_charts_frame = customtkinter.CTkFrame(charts_vertical_container)
        triple_charts_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Create three equal frames side by side
        food_type_frame = customtkinter.CTkFrame(triple_charts_frame,
                                                corner_radius=25, border_width=0)
        food_type_frame.pack(side="left", fill="both", expand=True, padx=5)

        sides_frame = customtkinter.CTkFrame(triple_charts_frame,
                                            corner_radius=25, border_width=0)
        sides_frame.pack(side="left", fill="both", expand=True, padx=5)

        beverages_frame = customtkinter.CTkFrame(triple_charts_frame,
                                                corner_radius=25, border_width=0)
        beverages_frame.pack(side="left", fill="both", expand=True, padx=5)

        ### Now prepare the data to plot ###

        # Fetch event data for top charts 
        event_counts = self.get_event_counts()
        event_types = list(event_counts.keys())
        counts = list(event_counts.values())

        # -- Top - Bar chart (Most Selected Events) --
        fig1, ax1 = plt.subplots(figsize=(3, 3), dpi=100)
        ax1.bar(event_types, counts, color="#1f6aa5")
        ax1.set_title("Most Selected Events", color="white")
        ax1.set_xlabel("Events", color="white")
        ax1.set_ylabel("Number of Selections", color="white")
        ax1.tick_params(axis='x', rotation=0, colors='white')
        ax1.tick_params(axis='y', colors='white')
        fig1.patch.set_facecolor('#333333')
        ax1.set_facecolor('white')
        plt.tight_layout()

        canvas1 = FigureCanvasTkAgg(fig1, master=bar_chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # -- Top - Pie chart (Total Events) --
        fig2, ax2 = plt.subplots(figsize=(3, 3), dpi=100)
        ax2.pie(counts, labels=event_types, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax2.set_title("Total Events", color="white")
        fig2.patch.set_facecolor('#333333')
        ax2.set_facecolor('white')
        plt.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=pie_chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # -- Bottom - Line chart for total_price over time --
        try:
            with sqlite3.connect("events.db") as conn:
                c = conn.cursor()
                c.execute("SELECT total_price FROM total_of_sales ORDER BY id ASC")
                total_prices = [row[0] for row in c.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch sales data: {e}")
            total_prices = []

        x_vals = list(range(1, len(total_prices) + 1))

        fig3, ax3 = plt.subplots(figsize=(6, 2.5), dpi=100)
        ax3.plot(x_vals, total_prices, marker='o', linestyle='-', color='green')
        ax3.set_title("Total Sales Over Time", color="white")
        ax3.set_xlabel("Sale Number", color="white")
        ax3.set_ylabel("Total Price (R)", color="white")
        ax3.tick_params(colors='white')
        fig3.patch.set_facecolor('#333333')
        ax3.set_facecolor('white')
        plt.tight_layout()

        canvas3 = FigureCanvasTkAgg(fig3, master=bottom_chart_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # For food_types, sides, beverages from total_of_sales, get counts
        try:
            with sqlite3.connect("events.db") as conn:
                c = conn.cursor()
                # Counts for food_type
                c.execute("SELECT food_type, COUNT(*) FROM total_of_sales GROUP BY food_type")
                food_data = c.fetchall()
                food_labels = [row[0] for row in food_data]
                food_counts = [row[1] for row in food_data]

                # Counts for sides
                c.execute("SELECT sides, COUNT(*) FROM total_of_sales GROUP BY sides")
                sides_data = c.fetchall()
                sides_labels = [row[0] for row in sides_data]
                sides_counts = [row[1] for row in sides_data]

                # Counts for beverages
                c.execute("SELECT beverages, COUNT(*) FROM total_of_sales GROUP BY beverages")
                bev_data = c.fetchall()
                bev_labels = [row[0] for row in bev_data]
                bev_counts = [row[1] for row in bev_data]
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch food/sides/beverages data: {e}")
            food_labels = food_counts = sides_labels = sides_counts = bev_labels = bev_counts = []

        # Food Type bar chart
        fig4, ax4 = plt.subplots(figsize=(3, 3), dpi=100)
        ax4.bar(food_labels, food_counts, color="#FF7F50")
        ax4.set_title("Food Types", color="white")
        ax4.tick_params(axis='x', rotation=0, colors='white')
        ax4.tick_params(axis='y', colors='white')
        fig4.patch.set_facecolor('#333333')
        ax4.set_facecolor('white')
        plt.tight_layout()

        canvas4 = FigureCanvasTkAgg(fig4, master=food_type_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Sides bar chart
        fig5, ax5 = plt.subplots(figsize=(3, 3), dpi=100)
        ax5.barh(sides_labels, sides_counts, color="#6A5ACD")
        ax5.set_title("Sides", color="white")
        ax5.tick_params(axis='x', rotation=0, colors='white')
        ax5.tick_params(axis='y', colors='white')
        fig5.patch.set_facecolor('#333333')
        ax5.set_facecolor('white')
        plt.tight_layout()

        canvas5 = FigureCanvasTkAgg(fig5, master=sides_frame)
        canvas5.draw()
        canvas5.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Beverages bar chart
        fig6, ax6 = plt.subplots(figsize=(3, 3), dpi=100)
        ax6.bar(bev_labels, bev_counts, color="#20B2AA")
        ax6.set_title("Beverages", color="white")
        ax6.tick_params(axis='x', rotation=10, colors='white')
        ax6.tick_params(axis='y', colors='white')
        fig6.patch.set_facecolor('#333333')
        ax6.set_facecolor('white')
        plt.tight_layout()

        canvas6 = FigureCanvasTkAgg(fig6, master=beverages_frame)
        canvas6.draw()
        canvas6.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    def get_event_counts(self):
        """Fetch the count of each event type from the database."""
        event_counts = {}
        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            c.execute("SELECT category, COUNT(*) FROM events GROUP BY category")  # Group by event category
            rows = c.fetchall()  # Fetch all results
        for row in rows:
            event_counts[row[0]] = row[1]  # Map event category to its count
        return event_counts   
        
    '''Function to display saved events in a list'''
    def show_saved_events(self):
        self.clear_content()  # Clear previous content
        self.title("Event Planner | Events")  # Update window title

        # Search input for filtering events
        self.search_input = customtkinter.CTkEntry(self.form_frame_content, placeholder_text="Search Event ...", corner_radius=20,
                                                  width=800, border_width=1, fg_color="white", text_color="black")
        self.search_input.pack(padx=10, pady=10)  # Add search input to the form
        
        # Bind KeyRelease event to call search_events when user types
        self.search_input.bind("<KeyRelease>", lambda event: self.search_events())

        # Frame for the events table
        table_frame = customtkinter.CTkFrame(self.form_frame_content, width=0)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview for displaying events
        self.tree = ttk.Treeview(table_frame, columns=("Id" ,"Category", "Date", "Time", "Location", "Client Name","Client Email", "Description"), show="headings")
        for col in ("Id","Category", "Date", "Time", "Location", "Client Name", "Client Email","Description"):
            self.tree.heading(col, text=col)  # Set column headings
            self.tree.column(col, width=150 if col in ["email", "Description"] else 100)  # Set column widths

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
        
    def search_events(self):
        if self.debounce_timer:
            self.after_cancel(self.debounce_timer)  # Cancel the previous timer
        # Set a new timer to call the actual search function after 300ms
        self.debounce_timer = self.after(300, self.perform_search)
        
    def perform_search(self):
        search_term = self.search_input.get().strip()
        # Clear the current treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        if not search_term:
            self.load_events_into_tree()  # Show all events if search term is empty
            return
        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            query = """
                SELECT * FROM events
                WHERE category LIKE ? OR
                    client_email LIKE ? OR
                    location LIKE ? OR
                    client_name LIKE ?
            """
            search_pattern = f"%{search_term}%"
            c.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            results = c.fetchall()
        for event in results:
            self.tree.insert("", "end", values=event)

    '''Function to load guests from the database into the treeview'''
    def load_guests_into_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear existing rows in the treeview

        with sqlite3.connect("events.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM guests")  # Query to select all events
            events = c.fetchall()  # Fetch all events

        for event in events:
            self.tree.insert("", "end", values=event)  # Insert each event into the treeview

    '''Function to display saved events in a list'''
    def show_saved_guests(self):
        from generate_invitations import generate_invitation_for_selected_guest
        self.clear_content()  # Clear previous content
        self.title("Event Planner | Guests")  # Update window title

        # Frame for the events table
        table_frame = customtkinter.CTkFrame(self.form_frame_content, width=0)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview for displaying events
        self.tree = ttk.Treeview(table_frame, columns=("Id" ,"category", "name", "email", "client_id", "client_name", "client_email"), show="headings")
        for col in ("Id" ,"category", "name", "email", "client_id", "client_name", "client_email"):
            self.tree.heading(col, text=col)  # Set column headings
            self.tree.column(col, width=150 if col in ["name", "email"] else 100)  # Set column widths

        self.tree.pack(fill="both", expand=True)  # Add the treeview to the table frame
        self.load_guests_into_tree()  # Load events from the database into the treeview

        # Bind the selection event to update the selected event
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.update_selected_guest())

        # Frame for action buttons
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.pack(pady=10)

        # Button to create a Guest
        guest_add = customtkinter.CTkButton(btn_frame, text="Add Guests",command=self.toggle_createGuestForm)
        guest_add.grid(row=0, column=0, pady=(0, 0), padx=(0, 0))

        # Button to create a new event
        delete_btn = customtkinter.CTkButton(btn_frame, text="Invitations", command=lambda:generate_invitation_for_selected_guest(self.tree))
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
                client_id=data[0],
                category=data[1],
                date=data[2],
                time=data[3],
                location=data[4],
                client_name=data[5],
                client_email=data[6],
                description=data[7]  # Pass the event details to the modify events form
            )
            modifyEvents_instance.mainloop()  # Run the modify events GUI

    '''Function to update the selected guest in the treeview'''
    def update_selected_guest(self):
        selected_item = self.tree.focus()  # Get the currently selected item
        if not selected_item:
            messagebox.showwarning("Select Event", "Please select an guest to update.")  # Show warning if no guest is selected
            return

        data = self.tree.item(selected_item)["values"]  # Get the values of the selected guest
        if data:
            from modifyGuestForm import App as modifyGuest  # Import the modify events GUI
            modifyEvents_instance = modifyGuest()  # Create an instance of the modify events GUI
            modifyEvents_instance.show_guest_form(
                guest_id=data[0],
                category=data[1],
                name=data[2],
                email=data[3],
                client_id=data[4]
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
            c.execute("DELETE FROM events WHERE client_id=?", (data[0]))  # Delete the event
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