import json
from pathlib import Path

import pytest

import storage
from contact import Contact


@pytest.fixture
def contacts_file(tmp_path, monkeypatch):
    path = tmp_path / "contacts.json"
    monkeypatch.setattr(storage, "CONTACTS_FILE", str(path))
    return path


def test_load_missing_file_starts_empty(contacts_file, capsys):
    assert storage.load_contacts() == []
    assert not contacts_file.exists()
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "contents",
    [
        pytest.param(b"", id="empty-file"),
        pytest.param(b'[{"Name":', id="truncated-json"),
        pytest.param(b"not JSON", id="invalid-json"),
        pytest.param(
            b"\xff",
            id="invalid-utf8",
            marks=pytest.mark.xfail(
                strict=True,
                raises=UnicodeDecodeError,
                reason="Invalid UTF-8 escapes the file-read error handler.",
            ),
        ),
        pytest.param(
            b"null",
            id="json-null",
            marks=pytest.mark.xfail(
                strict=True,
                raises=TypeError,
                reason="The loader attempts to iterate a null JSON value.",
            ),
        ),
        pytest.param(
            b"{}",
            id="json-object",
            marks=pytest.mark.xfail(
                strict=True,
                raises=AssertionError,
                reason="An empty JSON object is silently treated as a contact list.",
            ),
        ),
    ],
)
def test_load_corrupt_file_warns_and_starts_empty(contacts_file, capsys, contents):
    contacts_file.write_bytes(contents)

    assert storage.load_contacts() == []
    assert "Warning:" in capsys.readouterr().out
    assert contacts_file.read_bytes() == contents


def test_load_unreadable_path_warns_and_starts_empty(contacts_file, capsys):
    contacts_file.mkdir()

    assert storage.load_contacts() == []
    assert "Warning:" in capsys.readouterr().out


def test_load_skips_bad_records_and_defaults_optional_fields(contacts_file, capsys):
    first = {
        "Name": " Alice ",
        "Phone Number": " 12345678 ",
        "Email": " alice@example.com ",
    }
    last = {
        "Name": "Bob",
        "Phone Number": "+1 (234) 5678",
        "Email": "bob@example.com",
        "Favorite": True,
    }
    records = [
        first,
        {"Name": "Missing fields"},
        {**last, "Email": "bad address"},
        None,
        last,
    ]
    contacts_file.write_text(json.dumps(records), encoding="utf-8")

    contacts = storage.load_contacts()

    assert [contact.name for contact in contacts] == ["Alice", "Bob"]
    alice, bob = contacts
    assert (alice.phone_number, alice.email) == ("12345678", "alice@example.com")
    assert (alice.address, alice.birthday, alice.notes, alice.favorite) == (
        "", "", "", False,
    )
    assert bob.favorite is True
    assert capsys.readouterr().out.count("Warning: skipped an invalid saved contact") == 3


def test_save_and_load_round_trip(contacts_file):
    contacts = [
        Contact(
            "Zoë Smith", "+1 (555) 123-4567", "zoe@example.com",
            address="14 Rue de l’Église", birthday="1999-04-21",
            notes="Met at PyCon\nFollow up", favorite=True,
        ),
        Contact("Bob", "12345678", "bob@example.com"),
    ]

    storage.save_contacts(contacts)

    expected = [
        {
            "Name": "Zoë Smith",
            "Phone Number": "+1 (555) 123-4567",
            "Email": "zoe@example.com",
            "Address": "14 Rue de l’Église",
            "Birthday": "1999-04-21",
            "Notes": "Met at PyCon\nFollow up",
            "Favorite": True,
        },
        {
            "Name": "Bob",
            "Phone Number": "12345678",
            "Email": "bob@example.com",
            "Address": "",
            "Birthday": "",
            "Notes": "",
            "Favorite": False,
        },
    ]
    assert json.loads(contacts_file.read_text(encoding="utf-8")) == expected
    assert [contact.to_dict() for contact in storage.load_contacts()] == expected
    assert list(contacts_file.parent.iterdir()) == [contacts_file]


def test_save_empty_list_replaces_previous_data(contacts_file, capsys):
    storage.save_contacts([Contact("Alice", "12345678", "alice@example.com")])

    storage.save_contacts([])

    assert json.loads(contacts_file.read_text(encoding="utf-8")) == []
    assert storage.load_contacts() == []
    assert capsys.readouterr().out == ""


def test_failed_replace_preserves_previous_data_and_removes_temp_file(
    contacts_file, monkeypatch,
):
    original = Contact("Alice", "12345678", "alice@example.com")
    replacement = Contact("Bob", "87654321", "bob@example.com")
    storage.save_contacts([original])
    original_contents = contacts_file.read_bytes()

    def fail_replace(source, destination):
        staged = Path(source)
        assert staged.parent == contacts_file.parent
        assert destination == str(contacts_file)
        assert json.loads(staged.read_text(encoding="utf-8")) == [replacement.to_dict()]
        raise OSError("replace failed")

    monkeypatch.setattr(storage.os, "replace", fail_replace)
    with pytest.raises(OSError, match="replace failed"):
        storage.save_contacts([replacement])

    assert contacts_file.read_bytes() == original_contents
    assert list(contacts_file.parent.iterdir()) == [contacts_file]
