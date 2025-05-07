import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import messagebox, filedialog
import os

def generate_invitation_for_selected_guest(guest_tree):
    # Get the selected guest from the Treeview
    selected = guest_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a guest.")
        return

    # Extract guest details (adjust index if needed)
    guest_info = guest_tree.item(selected[0], "values")
    guest_email = guest_info[3]  # Guest's email address

    # Compose the email content
    subject = "You're Invited!"
    body = (
        f"Hi {guest_info[2]},\n\n"  # guest_info[2] = guest's name
        f"You are invited to the event: {guest_info[1]}.\n\n"  # guest_info[1] = event name
        "Please find attached invitation and confirm your attendance by replying to this email.\n\n"
        "Best regards,\n"
        "Event Organizer"
    )

    # Email credentials (use app password or environment vars in production)
    sender_email = "tembanithulisa2@gmail.com"
    sender_password = "mqnd djhq eixf owpa"

    # Prompt the user to select the invitation file (PDF/image/etc.)
    file_path = filedialog.askopenfilename(
        title="Select Invitation File",
        filetypes=[("PDF files", "*.pdf"), ("Image files", "*.png"), ("All files", "*.*")]
    )

    # If user cancels file selection
    if not file_path:
        messagebox.showinfo("Cancelled", "No file selected. Invitation not sent.")
        return

    try:
        # Create the email message object
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = guest_email
        msg["Subject"] = subject

        # Attach the text body
        msg.attach(MIMEText(body, "plain"))

        # Read and attach the selected file
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}",
            )
            msg.attach(part)

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login
            server.send_message(msg)  # Send the composed message

        # Inform the user of success
        messagebox.showinfo("Success", f"Invitation sent to {guest_email}")

    except Exception as e:
        # Show an error message if anything goes wrong
        messagebox.showerror("Error", f"Failed to send email:\n{str(e)}")
