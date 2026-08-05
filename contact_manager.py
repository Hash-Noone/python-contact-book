from contact import Contact

class ContactManager:
    def __init__(self, contacts=None):
        self.contacts = contacts if contacts is not None else []

    def add_contact(self, contact):
        if not isinstance(contact, Contact):
            raise ValueError("Only Contact instances can be added.")
        self.contacts.append(contact)

    def view_contacts(self):
        for contact in self.contacts.copy():
            fav_status = "Yes" if contact.favorite else "No"
            print(f" - {contact.name} (Phone: {contact.phone_number}, Email: {contact.email}) - Favorite: {fav_status}")
        
        return 

    def delete_contact(self, contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
        else:
            raise ValueError("Contact not found in the list.")