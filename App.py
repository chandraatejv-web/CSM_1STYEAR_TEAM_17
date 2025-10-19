import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        # Contacts will be a list of dictionaries with keys: 'name', 'phone', 'email'
        self.contacts = []

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Left frame for listbox
        frame_left = tk.Frame(self.root)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.contact_listbox = tk.Listbox(frame_left, width=30)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)

        scrollbar = tk.Scrollbar(frame_left)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_listbox.yview)

        # Right frame for details and buttons
        frame_right = tk.Frame(self.root)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame_right, text="Name:").grid(row=0, column=0, sticky='e')
        tk.Label(frame_right, text="Phone:").grid(row=1, column=0, sticky='e')
        tk.Label(frame_right, text="Email:").grid(row=2, column=0, sticky='e')

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.entry_name = tk.Entry(frame_right, textvariable=self.name_var, width=30)
        self.entry_phone = tk.Entry(frame_right, textvariable=self.phone_var, width=30)
        self.entry_email = tk.Entry(frame_right, textvariable=self.email_var, width=30)

        self.entry_name.grid(row=0, column=1, pady=5, sticky='w')
        self.entry_phone.grid(row=1, column=1, pady=5, sticky='w')
        self.entry_email.grid(row=2, column=1, pady=5, sticky='w')

        # Buttons
        btn_frame = tk.Frame(frame_right)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.btn_add = tk.Button(btn_frame, text="Add", command=self.add_contact)
        self.btn_edit = tk.Button(btn_frame, text="Edit", command=self.edit_contact)
        self.btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete_contact)
        self.btn_save = tk.Button(btn_frame, text="Save to File", command=self.save_to_file)
        self.btn_load = tk.Button(btn_frame, text="Load from File", command=self.load_from_file)

        self.btn_add.pack(side=tk.LEFT, padx=5)
        self.btn_edit.pack(side=tk.LEFT, padx=5)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        self.btn_load.pack(side=tk.LEFT, padx=5)

    def refresh_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, contact['name'])

    def on_contact_select(self, event):
        if not self.contact_listbox.curselection():
            return
        index = self.contact_listbox.curselection()[0]
        contact = self.contacts[index]
        self.name_var.set(contact['name'])
        self.phone_var.set(contact['phone'])
        self.email_var.set(contact['email'])

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Name is required.")
            return

        self.contacts.append({'name': name, 'phone': phone, 'email': email})
        self.refresh_contact_list()
        self.clear_entries()

    def edit_contact(self):
        if not self.contact_listbox.curselection():
            messagebox.showwarning("Select Contact", "Please select a contact to edit.")
            return

        index = self.contact_listbox.curselection()[0]
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Name is required.")
            return

        self.contacts[index] = {'name': name, 'phone': phone, 'email': email}
        self.refresh_contact_list()

    def delete_contact(self):
        if not self.contact_listbox.curselection():
            messagebox.showwarning("Select Contact", "Please select a contact to delete.")
            return

        index = self.contact_listbox.curselection()[0]
        contact = self.contacts[index]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete contact '{contact['name']}'?")
        if confirm:
            del self.contacts[index]
            self.refresh_contact_list()
            self.clear_entries()

    def clear_entries(self):
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')

    def save_to_file(self):
        filename = simpledialog.askstring("Save As", "Enter filename to save (e.g., contacts.txt):")
        if not filename:
            return
        try:
            with open(filename, 'w') as f:
                for c in self.contacts:
                    line = f"{c['name']},{c['phone']},{c['email']}\n"
                    f.write(line)
            messagebox.showinfo("Saved", f"Contacts saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def load_from_file(self):
        filename = simpledialog.askstring("Load File", "Enter filename to load (e.g., contacts.txt):")
        if not filename:
            return
        try:
            with open(filename, 'r') as f:
                self.contacts.clear()
                for line in f:
                    name, phone, email = line.strip().split(',', 2)
                    self.contacts.append({'name': name, 'phone': phone, 'email': email})
            self.refresh_contact_list()
            self.clear_entries()
            messagebox.showinfo("Loaded", f"Contacts loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
