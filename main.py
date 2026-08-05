from storage import load_contacts, save_contacts
from contact import Contact
from contact_manager import ContactManager

contacts = load_contacts()  
contact_manager = ContactManager(contacts)

while True:
    print("\n===== Contact Manager =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Toggle Favorite")
    print("4. Delete Contact")
    print("5. Save and Exit")

    choice = input("Choose: ")

    match choice:
        case "1":#add contact
            name = input("Enter contact name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            birthday = input("Enter birthday: ")
            notes = input("Enter notes: ")
            favorite = input("Is favorite? (y/n): ").lower() == "y"
            contact = Contact(name, phone_number, email, address, birthday, notes, favorite)
            contact_manager.add_contact(contact)
            print("Contact added successfully.")
            save_contacts(contact_manager.contacts)

        case "2":#view contacts
            if not contact_manager.contacts:
                print("No contacts available.")
            else:
                print("Contacts:")
                contact_manager.view_contacts()

        case "3":#toggle favorite
            if not contact_manager.contacts:
                print("No contacts available.")
            else:
                contact_manager.view_contacts()
            try:
                index = int(input("Enter contact number: ")) - 1
                if 0 <= index < len(contact_manager.contacts):
                    contact_manager.contacts[index].toggle_favorite()
                    save_contacts(contact_manager.contacts)
                    print("Favorite status updated.")
                else:
                    print("Invalid contact number.")
            except ValueError:
                print("Please enter a valid number.")
                continue

        case "4":#delete contact
            print("Contacts:")
            contact_manager.view_contacts()
            try:
                index = int(input("Enter contact number: ")) - 1
                if 0 <= index < len(contact_manager.contacts):
                    contact_manager.delete_contact(contact_manager.contacts[index])
                    save_contacts(contact_manager.contacts)
                    print("Contact deleted.")
                else:
                    print("Invalid contact number.")
            except ValueError:
                print("Please enter a valid number.")
                continue


        case "5":#save and exit
            save_contacts(contact_manager.contacts)
            print("Contacts saved. Goodbye!")
            break

        case _:
            print("Invalid choice.")