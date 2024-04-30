import unittest
import re

PHONE_PATTERN = r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?'
# todo: consider using this simplified and more robust regex
# PHONE_PATTERN = r'^\s*\+?[- ()\d]{10,14}\s*$'

class TestPhoneRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(PHONE_PATTERN)

    def test_valid_phones(self):
        valid_phones = [
            "+79130073119",
            "79130073119",
            "7-913-007 31 19",
            " 79130073119 ",
            "7:913:007:31:19",
            "7.913.007.31.19"
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
            "01234567890123456789"
        ]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertIsNone(self.regex.match(phone))
