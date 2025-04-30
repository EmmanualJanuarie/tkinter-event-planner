import customtkinter
import sys
import os
from tkinter import messagebox

sys.path.append(os.path.abspath("C:\\Users\\Emmanual.Januarie\\Documents\\GitHub\\tkinter-event-planner"))

customtkinter.set_appearance_mode("dark")  # Set dark mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("Event Planner | Create Quote")  # Title of the form
        self.geometry("360x520")  # dimensions of the form

        # Main content area
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True)

        self.form_frame_content = customtkinter.CTkFrame(self.form_frame, border_width=1)
        self.form_frame_content.pack(padx=20, pady=20, fill="both", expand=True)

        # Call the function to create the form and image
        self.show_quote_form()

    def clear_content(self):
        # Clear the content of the form
        for widget in self.form_frame_content.winfo_children():
            widget.destroy()

    def create_event_form(self):
        email = self.entry_email.get()
        food_type = self.entry_food_type.get()
        sides = self.entry_side_type.get()
        beverages = self.entry_beverage_type.get()
        guest_slider = self.entry_GuestSlider.get()

        if not all([email, food_type, sides, beverages, guest_slider]):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        # Here you would typically save the data to a database or process it
        # For demonstration, we'll just show a success message
        messagebox.showinfo("Success", "Quote created successfully!")

        # Clear the form after submission
        self.entry_email.delete(0, 'end')
        self.entry_food_type.set('')  # Clear the combo box selection
        self.entry_side_type.set('')
        self.entry_beverage_type.set('')
        self.entry_GuestSlider.set(1)  # Reset slider to default value

        # Update total price after submission
        self.update_total_price()

    def show_quote_form(self):
        self.clear_content()

        title = customtkinter.CTkLabel(self.form_frame_content, text="Create Quote", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input | Email
        self.entry_email = customtkinter.CTkEntry(self.form_frame_content, fg_color="white", placeholder_text="Email", corner_radius=20,
                                                  width=300, border_width=0, text_color='black')
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)

        # Label for Food Type
        self.lbl_foodtype = customtkinter.CTkLabel(self.form_frame_content, text="Select Food Type:")
        self.lbl_foodtype.grid(row=2, column=1, pady=(10, 0), padx=(0, 180))

        # Input | Food Type (Combo Box)
        self.entry_food_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Plated Dinner", "Buffet", "Spit Braai", "BBQ Buffet", "Comfort Food"],
                                                           corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_food_type.grid(row=3, column=1, pady=5, padx=10)

        # Label for SIDES Type
        self.lbl_sides = customtkinter.CTkLabel(self.form_frame_content, text="Select Side Type:")
        self.lbl_sides.grid(row=4, column=1, pady=(10, 0), padx=(0, 180))

        # Input | Side Type (Combo Box)
        self.entry_side_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                           values=["Wedding Pasteries", "Party Pasteries", "Snacks", "Breakfast Pastries",
                                                                   "Lunch Pastries", "Coffee break Pasteries", "Finger foods"], corner_radius=20, 
                                                           width=300, fg_color="white", text_color='black')
        self.entry_side_type.grid(row=5, column=1, pady=5, padx=10)

        # Label for Beverages Type
        self.lbl_beverages = customtkinter.CTkLabel(self.form_frame_content, text="Select Beverage:")
        self.lbl_beverages.grid(row=6, column=1, pady=(10, 0), padx=(0, 180))

        # Input | Beverage Type (Combo Box)
        self.entry_beverage_type = customtkinter.CTkComboBox(self.form_frame_content, 
                                                               values=["Soft Drinks(500ml)", "Soft Drinks(250ml)", "Soft Drinks(1.5l)" ,"Alcoholic Beverages", "Coffee & Tea", "Other Beverages"],
                                                               corner_radius=20, 
                                                               width=300, fg_color="white", text_color='black')
        self.entry_beverage_type.grid(row=7, column=1, pady=5, padx=10)

        # Slider for selecting amount of guests
        self.lbl_currentGuests = customtkinter.CTkLabel(self.form_frame_content, text="15")  # Default value

        # Label for Guest amount
        self.lbl_guestAmount = customtkinter.CTkLabel(self.form_frame_content, text=f"Guest Amount: {self.lbl_currentGuests.cget('text')}")
        self.lbl_guestAmount.grid(row=8, column=1, pady=(10, 0), padx=(0, 180))

        # Slider for selecting amount of guests
        self.entry_GuestSlider = customtkinter.CTkSlider(
            self.form_frame_content, 
            from_=15,  # Minimum number of guests
            to=100,   # Maximum number of guests
            command=self.update_guest_label  # Function to call when slider value changes
        )
        self.entry_GuestSlider.grid(row=9, column=1, pady=(10, 0), padx=(0, 70))

        # Total Price Label
        self.lbl_total_price = customtkinter.CTkLabel(self.form_frame_content, text="Total Price: R0.00", font=("Arial", 14, "bold"))
        self.lbl_total_price.grid(row=10, column=0, columnspan=2, pady=10)

        # Submit Button
        submit_btn = customtkinter.CTkButton(self.form_frame_content, text="Send Quote", command=self.create_event_form)
        submit_btn.grid(row=11, column=0, columnspan=2, pady=10)

    # Function to update the guest label based on slider value
    def update_guest_label(self, value):
        guest_count = int(value)
        self.lbl_currentGuests.configure(text=str(guest_count))  # Update label with current slider value
        self.lbl_guestAmount.configure(text=f"Guest Amount: {guest_count}")  # Update guest amount label
        self.update_total_price()  # Update total price when guest count changes

    # Function to calculate and update the total price
    def update_total_price(self):
        guest_count = int(self.entry_GuestSlider.get())
        food_type = self.entry_food_type.get()
        side_type = self.entry_side_type.get()
        beverage_type = self.entry_beverage_type.get()
        
        # pricing logic for 
        price_per_guest = 0

        '''conditional statement for price logic of food types'''
        if food_type == "Plated Dinner":
            price_per_guest = 30.00
        elif food_type == "Buffet":
            price_per_guest = 25.00
        elif food_type == "Spit Braai":
            price_per_guest = 28.25
        elif food_type == "BBQ Buffet":
            price_per_guest = 25.50
        elif food_type == "Comfort Food":
            price_per_guest = 30.00

        '''conditional statement for price logic of Side types'''
        if  side_type == "Wedding Pasteries":
            price_per_guest = 8.90
        elif side_type == "Party Pasteries":
            price_per_guest = 6.20
        elif side_type == "Snacks":
            price_per_guest = 5.20
        elif side_type == "Breakfast Pastries":
            price_per_guest = 8.20
        elif side_type == "Lunch Pastries":
            price_per_guest = 7.00
        elif side_type == "Coffee break Pasteries":
            price_per_guest = 7.10
        elif side_type == "Finger foods":
            price_per_guest = 6.25

        '''conditional statement for price logic of Beverage types'''
        if  beverage_type == "Soft Drinks(500ml)":
            price_per_guest = 10.20
        elif beverage_type == "Soft Drinks(250ml)":
            price_per_guest = 5.20
        elif beverage_type == "Soft Drinks(1.5l)":
            price_per_guest = 25.00
        elif beverage_type == "Alcoholic Beverages":
            price_per_guest = 25.00
        elif beverage_type == "Coffee & Tea":
            price_per_guest = 10.00
        elif beverage_type == "Other Beverages":
            price_per_guest = 10.00

        total_price = guest_count * price_per_guest
        self.lbl_total_price.configure(text=f"Total Price: R{total_price:.2f}")  # Update total price label

if __name__ == "__main__":
    app = App()
    app.mainloop()
