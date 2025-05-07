import customtkinter
import sys
import os
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from tkinter import filedialog


sys.path.append(os.path.abspath("C:\\Users\\Emmanual.Januarie\\Documents\\GitHub\\tkinter-event-planner"))

customtkinter.set_appearance_mode("dark")  # Set dark mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("Event Planner | Create Quote")  # Title of the form
        self.geometry("380x580")  # dimensions of the form

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

    def email_exists(self, email):
        # Connect to your local sqlite DB and check if email exists in users table
        try:
            conn = sqlite3.connect('events.db')  
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM events WHERE client_email = ?", (email,))
            exists = cursor.fetchone()[0] > 0
            conn.close()
            return exists
        except Exception as e:
            messagebox.showerror("Database Error", f"Error checking client_email in database: {str(e)}")
            return False
       # Function to print pdf
    def print_pdf(self):
        email = self.entry_email.get()
        food_type = self.entry_food_type.get()
        sides = self.entry_side_type.get()
        beverages = self.entry_beverage_type.get()
        guest_count = int(self.entry_GuestSlider.get())
        total_price = self.calculate_total_price(food_type, sides, beverages, guest_count)

        # Ask user where to save the PDF
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not filepath:
            return  # User canceled the save dialog

        # Create the PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        margin_x = 50
        margin_y = 50
        line_height = 25
        y = height - margin_y

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, y, "Event Quote Summary")
        y -= line_height * 2

        c.setFont("Helvetica", 12)
        lines = [
            f"Client Email: {email}",
            f"Food Type: {food_type}",
            f"Side Type: {sides}",
            f"Beverage Type: {beverages}",
            f"Guest Count: {guest_count}",
            f"Total Price: R{total_price:.2f}"
        ]

        for line in lines:
            c.drawString(margin_x, y, line)
            y -= line_height

        c.save()

        messagebox.showinfo("PDF Saved", f"Quote PDF saved successfully at:\n{filepath}")

        # Open the PDF file automatically
        try:
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror("Open PDF Error", f"Could not open PDF:\n{e}")
    

    def send_quote_email(self, email, food_type, sides, beverages, guest_count, total_price):
        try:
            # SMTP server configuration - replace with your actual details
            smtp_server = 'smtp.gmail.com'  # Update with your SMTP server
            smtp_port = 587  # Update with your SMTP port
            smtp_user = 'ganatallyta@gmail.com'  # Update with your email
            smtp_password = 'srvp lslg puzb zfdf'  # Update with your email password

            subject = "Your Event Quote from Our Event Planner"
            body = f"""
                        Dear Valued Client,

                        Thank you for your interest in our event planning services. Please find below your personalized quote:

                        Food Type: {food_type}
                        Side Type: {sides}
                        Beverage Type: {beverages}
                        Guest Count: {guest_count}
                        Total Price: R{total_price:.2f}

                        If you have any questions or would like to proceed with this quote, please reply to this email or contact us at your convenience.

                        We look forward to helping you create a memorable event!

                        Best regards,
                        Your Event Planning Team
                                    """

            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))


            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            messagebox.showinfo("Success", f"Quote sent to {email}!")
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email: {str(e)}")

    def clear_form(self):
        self.entry_email.delete(0, 'end')
        self.entry_food_type.set('')
        self.entry_side_type.set('')
        self.entry_beverage_type.set('')
        self.entry_GuestSlider.set(15)
        self.lbl_total_price.configure(text="Total Price: R0.00")

    def calculate_total_price(self, food_type, sides, beverages, guest_count):
        price_per_guest = 0.0

        # Pricing logic for food types
        if food_type == "Plated Dinner":
            price_per_guest += 30.00
        elif food_type == "Buffet":
            price_per_guest += 25.00
        elif food_type == "Spit Braai":
            price_per_guest += 28.25
        elif food_type == "BBQ Buffet":
            price_per_guest += 25.50
        elif food_type == "Comfort Food":
            price_per_guest += 30.00

        # Pricing logic for side types
        if sides == "Wedding Pasteries":
            price_per_guest += 8.90
        elif sides == "Party Pasteries":
            price_per_guest += 6.20
        elif sides == "Snacks":
            price_per_guest += 5.20
        elif sides == "Breakfast Pastries":
            price_per_guest += 8.20
        elif sides == "Lunch Pastries":
            price_per_guest += 7.00
        elif sides == "Coffee break Pasteries":
            price_per_guest += 7.10
        elif sides == "Finger foods":
            price_per_guest += 6.25

        # Pricing logic for beverage types
        if beverages == "Soft Drinks(500ml)":
            price_per_guest += 10.20
        elif beverages == "Soft Drinks(250ml)":
            price_per_guest += 5.20
        elif beverages == "Soft Drinks(1.5l)":
            price_per_guest += 25.00
        elif beverages == "Alcoholic Beverages":
            price_per_guest += 25.00
        elif beverages == "Coffee & Tea":
            price_per_guest += 10.00
        elif beverages == "Other Beverages":
            price_per_guest += 10.00

        total_price = guest_count * price_per_guest
        return total_price

    def create_event_form(self):
        email = self.entry_email.get()
        food_type = self.entry_food_type.get()
        sides = self.entry_side_type.get()
        beverages = self.entry_beverage_type.get()
        guest_count = int(self.entry_GuestSlider.get())

        if not all([email, food_type, sides, beverages, guest_count]):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        # Check if the email exists in the database
        if not self.email_exists(email):
            messagebox.showerror("Email Error", "The entered email does not exist in our records.")
            return

        # Calculate total price
        total_price = self.calculate_total_price(food_type, sides, beverages, guest_count)

        # Send the quote email
        self.send_quote_email(email, food_type, sides, beverages, guest_count, total_price)

        # Show success message
        messagebox.showinfo("Success", "Quote created and sent successfully!")

        # Clear the form after submission
        self.clear_form()

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
        self.entry_GuestSlider.set(15)  # Default
        self.entry_GuestSlider.grid(row=9, column=1, pady=(10, 0), padx=(0, 70))

        # Total Price Label
        self.lbl_total_price = customtkinter.CTkLabel(self.form_frame_content, text="Total Price: R0.00", font=("Arial", 14, "bold"))
        self.lbl_total_price.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Button frame
        btn_frame = customtkinter.CTkFrame(self.form_frame_content, fg_color="#333333")
        btn_frame.grid(row=11, column=0, columnspan=2, pady=10)

        submit_quote_btn = customtkinter.CTkButton(btn_frame, text="Send Quote",  command=self.create_event_form)
        submit_quote_btn.grid(row=0, column=0, pady=10, padx=20)

        print_pdf_btn = customtkinter.CTkButton(btn_frame, text="Print PDF", command=self.print_pdf)
        print_pdf_btn.grid(row=0, column=1, pady=10)

    # Function to update the guest label based on slider value
    def update_guest_label(self, value):
        guest_count = int(value)
        self.lbl_currentGuests.configure(text=str(guest_count))  # Update label with current slider value
        self.lbl_guestAmount.configure(text=f"Guest Amount: {guest_count}")  # Update guest amount label
        self.update_total_price()  # Update total price when guest count changes

    # Function to calculate and update the total price shown on the label
    def update_total_price(self):
        guest_count = int(self.entry_GuestSlider.get())
        food_type = self.entry_food_type.get()
        side_type = self.entry_side_type.get()
        beverage_type = self.entry_beverage_type.get()
        if all([food_type, side_type, beverage_type]):
            total_price = self.calculate_total_price(food_type, side_type, beverage_type, guest_count)
        else:
            total_price = 0.0
        self.lbl_total_price.configure(text=f"Total Price: R{total_price:.2f}")  # Update total price label

if __name__ == "__main__":
    app = App()
    app.mainloop()