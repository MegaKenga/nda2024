import unittest
import re

EMAIL_PATTERN = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]{2,})'
# todo: write more test cases, improve pattern


class TestEmailRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(EMAIL_PATTERN)

    def test_valid_emails(self):
        valid_emails = [
            "a@b.com",
            "a.b@c.d.ru",
            "adsfsdfsf.bgfdgdfg12@cdgfdfgd25.ddfgdgf25.ru ",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertIsNotNone(self.regex.match(email))

    def test_invalid_emails(self):
        invalid_emails = [
            "a@b",
            "a@b.c",
            "abc",
            "a@b@c",
            ""
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertIsNone(self.regex.match(email))


if __name__ == '__main__':
    unittest.main()
