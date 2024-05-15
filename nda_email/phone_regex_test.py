import unittest
import re

from nda_email.forms import PHONE_PATTERN


class TestPhoneRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(PHONE_PATTERN)

    def test_valid_phones(self):
        valid_phones = [
            "+79130073119",
            "79130073119",
            "7-913-0073119",
            "7:913:007:31:19",
            "7.913.007.31.19",
            "083 120 56 20",
            "8(846)2569888",
            "8(3432)5698888"
        ]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertIsNotNone(self.regex.match(phone))

    def test_invalid_phones(self):
        invalid_phones = [
            "+7913007311g",
            "7913@0073119",
            "5573212",
            "332 12 07",
            "01234567890123456789",
            "+7  91 3   007 31  1   9",
            "84456464641g"
            "898553@10868"
            ""
        ]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertIsNone(self.regex.match(phone))


if __name__ == '__main__':
    unittest.main()
