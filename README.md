# 📒 Contact Manager

A simple command-line contact manager written in Python. It stores, edits, searches and manages contacts using object-oriented programming and a local JSON file.

## Features

- Add a new contact (name, phone, email, address, birthday, notes, favorite)
- Update an existing contact (a blank answer keeps the current value)
- View all contacts
- Search contacts by name (case-insensitive, partial matches)
- Mark or unmark contacts as favorites (shown with a ★)
- Delete contacts
- Phone number and email validation; only the bad field is asked again
- Contacts are saved automatically after every change and loaded on startup

## Requirements

- Python 3.10 or later
- No third-party packages (standard library only)

## How to Run

```bash
git clone https://github.com/Hash-Noone/python-contact-book.git
cd python-contact-book
python3 main.py
```

## Usage

Pick an option by typing its number and pressing Enter:

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

Example session (adding a contact, then listing it):

```
Choose: 1
Enter contact name: Alice Smith
Enter phone number: +1 555-123-4567
Enter email: alice@example.com
Enter address:
Enter birthday: 1999-04-21
Enter notes: Met at PyCon
Is favorite? (y/n) [n]: y
Contact added successfully.

Choose: 3
Contacts:
1. ★ Alice Smith (Phone: +1 555-123-4567, Email: alice@example.com)
```

Update, Toggle Favorite and Delete first list the contacts and ask for a contact number; leave it blank to cancel.

## Validation Rules

| Field | Rule |
|-------|------|
| Name | Required, at least 2 characters |
| Phone | Required; digits, spaces, `(`, `)`, `-` and an optional leading `+`; 8 to 15 digits; balanced parentheses |
| Email | Required; `local@domain.tld` with a simplified RFC 5322 check (local part up to 64 characters, whole address up to 254) |
| Address, birthday, notes | Optional free text |

## Data Storage

Contacts are saved to `contacts.json` in the same folder as the program files, whatever directory you run it from. The file is created on the first save and is listed in `.gitignore`, so your personal contacts are never committed. Delete it to start with an empty contact list.

Each contact is stored as a JSON object:

```json
[
    {
        "Name": "Alice Smith",
        "Phone Number": "+1 555-123-4567",
        "Email": "alice@example.com",
        "Address": "",
        "Birthday": "1999-04-21",
        "Notes": "Met at PyCon",
        "Favorite": true
    }
]
```

- Saves are atomic: data is written to a temporary file that then replaces `contacts.json`, so a crash mid-save cannot corrupt existing contacts.
- On startup, a record that is missing required fields or fails validation is skipped with a warning; the other contacts still load.

## Project Structure

```
python-contact-book/
├── main.py              # Command-line menu, prompts and output (the only file that uses input/print)
├── contact.py           # Contact class and the name/phone/email validators
├── contact_manager.py   # ContactManager: add / update / delete / search / toggle favorite
├── storage.py           # Loading and saving contacts.json
├── contacts.json        # Created automatically on first save (git-ignored)
├── .gitignore
└── README.md
```

How the pieces fit together:

1. `main.py` loads saved contacts through `storage.load_contacts()` and hands them to a `ContactManager`.
2. Each menu option collects input, using the validators from `contact.py` to re-prompt on bad values.
3. The action calls a `ContactManager` method, then `storage.save_contacts()` writes the updated list to disk.

## Testing

There is no automated test suite yet. A quick smoke test pipes menu choices into the program (add a contact, view contacts, save and exit):

```bash
printf '1\nAlice\n5551234567\nalice@example.com\n\n\n\n\n3\n7\n' | python3 main.py
```

This saves a sample contact into the real `contacts.json`. If you already have saved contacts, back up `contacts.json` first and restore it afterwards (or run the test in a fresh clone). In a fresh clone, delete `contacts.json` afterwards to reset.

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
- Add automated tests

## Author

**Hash Noone**

GitHub: https://github.com/Hash-Noone
