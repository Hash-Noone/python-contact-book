# 📒 Contact Manager

A simple command-line Contact Manager built with Python. It stores, edits, searches and manages contacts using object-oriented programming and JSON file storage.

## Features

- Add a new contact (name, phone, email, address, birthday, notes)
- Update an existing contact (blank input keeps the current value)
- View all contacts
- Search contacts by name
- Mark or unmark contacts as favorites
- Delete contacts
- Phone number and email validation with re-prompting on bad input
- Contacts are saved automatically after every change and loaded on startup

## Project Structure

```
contact_manager/
│── main.py              # Command-line menu and user input
│── contact.py           # Contact class and field validation
│── contact_manager.py   # Add / update / delete / search logic
│── storage.py           # Loading and saving contacts.json
│── contacts.json        # Created automatically on first save
│── .gitignore
│── README.md
```

## Requirements

- Python 3.10 or later

## How to Run

```bash
git clone <repository-url>
cd contact_manager
python main.py
```

## Example

```
===== Contact Manager =====
1. Add Contact
2. Update Contact
3. View Contacts
4. Search Contacts
5. Toggle Favorite
6. Delete Contact
7. Save and Exit
Choose:
```

## Concepts Practiced

- Classes and objects (OOP)
- Separation of concerns (UI / logic / storage)
- Lists and dictionaries
- File handling and JSON serialization
- Regular expressions and input validation
- Exception handling

## Future Improvements

- Sort contacts alphabetically
- Filter favorite contacts
- Validate birthday format
- Detect duplicate contacts

## Author

**Hash Noone**

GitHub: https://github.com/Hash-Noone
