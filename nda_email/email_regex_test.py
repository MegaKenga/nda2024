
import unittest
import re

EMAIL_PATTERN = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
# todo: write more test cases, improve pattern


class TestEmailRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(EMAIL_PATTERN)

    def test_valid_emails(self):
        valid_emails = [
            "a@b.com",
            "a.b@c.d.ru",
            " a.b@c.d.ru ",
        ]
        for phone in valid_emails:
            with self.subTest(phone=phone):
                self.assertIsNotNone(self.regex.match(phone))

    def test_invalid_phones(self):
        invalid_emails = [
            "a@b",
            "a@b.c",
            "abc",
            "a@b@c",
            ""
        ]
        for phone in invalid_emails:
            with self.subTest(phone=phone):
                self.assertIsNone(self.regex.match(phone))
