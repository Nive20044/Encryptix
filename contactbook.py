import tkinter as tk
from tkinter import messagebox
import shelve

# Contact Book Application

class ContactBook:
    def _init_(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contact_db = shelve.open('contacts.db')

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Contact list
        self.contact_list = tk.Listbox(self.main_frame)
        self.contact_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=10, pady=10)
        self.contact_list.bind('<Double-1>', self.show_edit_contact_form)

        # Scrollbar for the contact list
        scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, padx=10, pady=10)
        self.contact_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_list.yview)

        # Buttons
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        add_btn = tk.Button(btn_frame, text="Add Contact", command=self.show_add_contact_form)
        add_btn.pack(side=tk.LEFT, padx=10)

        edit_btn = tk.Button(btn_frame, text="Edit Contact", command=self.show_edit_contact_form)
        edit_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = tk.Button(btn_frame, text="Delete Contact", command=self.delete_contact)
        delete_btn.pack(side=tk.LEFT, padx=10)

        search_entry = tk.Entry(btn_frame)
        search_entry.pack(side=tk.LEFT, padx=10)
        search_entry.bind('<KeyRelease>', self.search_contact)

        # Load contacts
        self.load_contacts()

    def load_contacts(self):
        self.contact_list.delete(0, tk.END)
        for contact in self.contact_db.values():
            self.contact_list.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def show_add_contact_form(self):
        ContactForm(self.root, self.contact_db, self.load_contacts)

    def show_edit_contact_form(self, event=None):
        selection = self.contact_list.curselection()
        if selection:
            index = selection[0]
            contact_key = list(self.contact_db.keys())[index]
            ContactForm(self.root, self.contact_db, self.load_contacts, contact_key)

    def delete_contact(self):
        selection = self.contact_list.curselection()
        if selection:
            index = selection[0]
            contact_key = list(self.contact_db.keys())[index]
            del self.contact_db[contact_key]
            self.load_contacts()

    def search_contact(self, event):
        query = event.widget.get().lower()
        self.contact_list.delete(0, tk.END)
        for contact in self.contact_db.values():
            if query in contact['name'].lower() or query in contact['phone']:
                self.contact_list.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def _del_(self):
        self.contact_db.close()

# Contact Form for adding/editing contacts

class ContactForm:
    def _init_(self, root, contact_db, refresh_callback, contact_key=None):
        self.root = tk.Toplevel(root)
        self.root.title("Contact Form")
        self.contact_db = contact_db
        self.refresh_callback = refresh_callback
        self.contact_key = contact_key

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        # If editing, load existing contact details
        if contact_key:
            contact = self.contact_db[contact_key]
            self.name_var.set(contact['name'])
            self.phone_var.set(contact['phone'])
            self.email_var.set(contact['email'])
            self.address_var.set(contact['address'])

        # Form fields
        tk.Label(self.root, text="Name:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.name_var).pack(pady=5)

        tk.Label(self.root, text="Phone:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.phone_var).pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.email_var).pack(pady=5)

        tk.Label(self.root, text="Address:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.address_var).pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save", command=self.save_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

    def save_contact(self):
        contact = {
            'name': self.name_var.get(),
            'phone': self.phone_var.get(),
            'email': self.email_var.get(),
            'address': self.address_var.get()
        }
        if self.contact_key:
            self.contact_db[self.contact_key] = contact
        else:
            contact_key = str(len(self.contact_db))
            self.contact_db[contact_key] = contact

        self.refresh_callback()
        self.root.destroy()

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
