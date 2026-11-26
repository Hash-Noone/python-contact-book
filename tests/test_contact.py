import pytest

from contact import Contact, validate_email, validate_name, validate_phone


@pytest.mark.parametrize(
    ("name", "expected"),
    [(" \tZoë Smith\n", "Zoë Smith"), (" Al ", "Al")],
)
def test_validate_name_strips_whitespace(name, expected):
    assert validate_name(name) == expected


@pytest.mark.parametrize(
    "name",
    [
        "",
        " \t",
        " A ",
        pytest.param(
            None,
            id="null",
            marks=pytest.mark.xfail(
                strict=True,
                raises=pytest.fail.Exception,
                reason="A null name is converted to the text 'None'.",
            ),
        ),
    ],
)
def test_validate_name_rejects_missing_or_short_names(name):
    with pytest.raises(ValueError):
        validate_name(name)


@pytest.mark.parametrize(
    ("phone", "expected"),
    [
        (" \t+1 (555) 123-4567 ", "+1 (555) 123-4567"),
        ("1234-5678", "1234-5678"),
        ("+123456789012345", "+123456789012345"),
    ],
)
def test_validate_phone_preserves_valid_formatting(phone, expected):
    assert validate_phone(phone) == expected


@pytest.mark.parametrize(
    "phone",
    [
        pytest.param("", id="empty"),
        pytest.param(12345678, id="non-text"),
        pytest.param("123-4567", id="seven-digits"),
        pytest.param("1234567890123456", id="sixteen-digits"),
        pytest.param("1234+5678", id="misplaced-plus"),
        pytest.param("1234x5678", id="letter"),
        pytest.param("1 (234 5678", id="missing-closing-parenthesis"),
        pytest.param(
            "1 )234( 5678",
            id="reversed-parentheses",
            marks=pytest.mark.xfail(
                strict=True,
                raises=pytest.fail.Exception,
                reason="Parentheses are counted without checking their order.",
            ),
        ),
    ],
)
def test_validate_phone_rejects_invalid_numbers(phone):
    with pytest.raises(ValueError):
        validate_phone(phone)


@pytest.mark.parametrize(
    "email",
    [
        "Alice.Smith+tag@sub.example-domain.com",
        f"{'a' * 64}@example.com",
        f"{'a' * 64}@{'b' * 63}.{'c' * 63}.{'d' * 58}.io",
    ],
    ids=["formatted", "64-character-local", "254-character-address"],
)
def test_validate_email_strips_whitespace(email):
    assert validate_email(f" \t{email}\n") == email


@pytest.mark.parametrize(
    "email",
    [
        pytest.param(None, id="non-text"),
        pytest.param("alice.example.com", id="missing-at-sign"),
        pytest.param("alice@example@com", id="extra-at-sign"),
        pytest.param("@example.com", id="empty-local"),
        pytest.param("alice..smith@example.com", id="consecutive-local-dots"),
        pytest.param("alice@-example.com", id="invalid-domain-label"),
        pytest.param("alice@example", id="missing-tld"),
        pytest.param("alice@example.c", id="short-tld"),
        pytest.param(f"{'a' * 65}@example.com", id="65-character-local"),
        pytest.param(
            f"{'a' * 64}@{'b' * 63}.{'c' * 63}.{'d' * 59}.io",
            id="255-character-address",
        ),
    ],
)
def test_validate_email_rejects_invalid_addresses(email):
    with pytest.raises(ValueError):
        validate_email(email)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [("name", "A"), ("phone_number", "abc"), ("email", "alice")],
)
def test_contact_checks_each_required_field(field, bad_value):
    fields = dict(name="Alice", phone_number="12345678", email="alice@example.com")
    fields[field] = bad_value

    with pytest.raises(ValueError):
        Contact(**fields)
