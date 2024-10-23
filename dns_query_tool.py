import dns.resolver
import dns.reversename
from tkinter import Tk, Label, Button, Entry, Frame, StringVar, ttk
from PIL import Image, ImageTk

# Function to perform DNS lookup for A, AAAA, CNAME, MX, TXT, NS, and SOA records
def dns_query(domain, record_type='A'):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(answer) for answer in answers]
    except dns.resolver.NoAnswer:
        return [f"No {record_type} records found for {domain}."]
    except dns.resolver.NXDOMAIN:
        return [f"The domain {domain} does not exist."]
    except Exception as e:
        return [f"Error occurred: {e}"]

# Function to perform reverse DNS lookup
def reverse_dns_lookup(ip_address):
    try:
        rev_name = dns.reversename.from_address(ip_address)
        domain_name = dns.resolver.resolve(rev_name, "PTR")[0]
        return f"Reverse DNS for {ip_address}: {domain_name}"
    except Exception as e:
        return f"Error occurred: {e}"

# Function to initialize the GUI
def init_gui():
    global domain_var, record_type_var, result_label, ip_var, gif_label

    # Create the main window
    root = Tk()
    root.title("DNS Query Tool")
    root.geometry("800x600")  # Set window size

    # Create a label to hold the GIF frames
    gif_label = Label(root)
    gif_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make label cover the entire window

    # Start the GIF playback
    play_gif()

    # Domain input
    domain_var = StringVar()
    domain_label = Label(root, text="Enter Domain Name:", bg="lightblue", font=("Arial", 12))
    domain_label.pack(pady=5)
    domain_entry = Entry(root, textvariable=domain_var, font=("Arial", 12))
    domain_entry.pack(pady=5)

    # Record type selection (Combobox)
    record_type_var = StringVar()
    record_type_label = Label(root, text="Select Record Type:", bg="lightblue", font=("Arial", 12))
    record_type_label.pack(pady=5)

    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']
    record_type_combobox = ttk.Combobox(root, textvariable=record_type_var, values=record_types, font=("Arial", 12))
    record_type_combobox.pack(pady=5)
    record_type_combobox.current(0)  # Set default selection to the first item

    # Query button
    query_button = Button(root, text="Query DNS", command=perform_dns_query, bg="blue", fg="white", font=("Arial", 12))
    query_button.pack(pady=10)

    # Clear button
    clear_button = Button(root, text="Clear", command=clear_fields, bg="red", fg="white", font=("Arial", 12))
    clear_button.pack(pady=5)

    # Result label
    result_label = Label(root, text="", bg="lightblue", wraplength=500, font=("Arial", 12))
    result_label.pack(pady=5)

    # Reverse DNS lookup input
    ip_var = StringVar()  # Initialize ip_var here
    ip_label = Label(root, text="Enter IP Address for Reverse DNS Lookup:", bg="lightblue", font=("Arial", 12))
    ip_label.pack(pady=5)
    ip_entry = Entry(root, textvariable=ip_var, font=("Arial", 12))
    ip_entry.pack(pady=5)

    # Reverse DNS button
    reverse_button = Button(root, text="Reverse DNS Lookup", command=perform_reverse_dns_lookup, bg="green", fg="white", font=("Arial", 12))
    reverse_button.pack(pady=10)

    # Start the GUI loop
    root.mainloop()

# Function to play GIF frames and fit them to the window
def play_gif():
    gif_image = Image.open("cn.gif")  # Update with your GIF path

    def update_frame(frame_num):
        gif_image.seek(frame_num)
        
        # Resize the frame to fit the label before converting to PhotoImage
        frame = gif_image.copy()  # Copy the current frame
        frame_resized = frame.resize((800, 600), Image.LANCZOS)  # Resize to window size
        photo_frame = ImageTk.PhotoImage(frame_resized)

        gif_label.configure(image=photo_frame)
        gif_label.image = photo_frame  # Keep a reference to avoid garbage collection
        frame_num += 1

        # Loop the GIF frames
        if frame_num >= gif_image.n_frames:
            frame_num = 0
        gif_label.after(100, update_frame, frame_num)

    update_frame(0)

# Function to perform DNS query and update the result label
def perform_dns_query():
    domain = domain_var.get()
    record_type = record_type_var.get().upper()
    result = dns_query(domain, record_type)
    result_label.config(text="\n".join(result))

# Function to perform reverse DNS lookup and update the result label
def perform_reverse_dns_lookup():
    ip_address = ip_var.get()
    result = reverse_dns_lookup(ip_address)
    result_label.config(text=result)

# Function to clear the input fields and result label
def clear_fields():
    domain_var.set("")
    ip_var.set("")
    result_label.config(text="")

# Main execution
if __name__ == "__main__":
    init_gui()