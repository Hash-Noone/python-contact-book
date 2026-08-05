import json
import os
from contact import Contact


def load_contacts():
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f:
            try:
                data = json.load(f)

                contacts = []

                for item in data:
                    contact = Contact(
                        name=item["Name"],
                        phone_number=item["Phone Number"],
                        email=item["Email"],
                        address=item["Address"],
                        birthday=item["Birthday"],
                        notes=item["Notes"],
                        favorite=item["Favorite"]
                    )
                    contacts.append(contact)

                return contacts

            except json.JSONDecodeError:
                return []

    return []


def save_contacts(contacts):
    data = [
        {
            "Name": contact.name,
            "Phone Number": contact.phone_number,
            "Email": contact.email,
            "Address": contact.address,
            "Birthday": contact.birthday,
            "Notes": contact.notes,
            "Favorite": contact.favorite,
        }
        for contact in contacts
    ]

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)