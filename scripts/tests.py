from django.test import TestCase
from django.template import Context, Template
from .models import Script


class ScriptModelTest(TestCase):
    def setUp(self):
        self.script = Script.objects.create(
            name='Test Script',
            description='Test description',
            code='<script>console.log("test");</script>',
            position='head',
            is_active=True,
            order=10
        )

    def test_script_creation(self):
        self.assertEqual(self.script.name, 'Test Script')
        self.assertEqual(self.script.position, 'head')
        self.assertTrue(self.script.is_active)

    def test_script_str_method(self):
        expected = 'Test Script (В <head>)'
        self.assertEqual(str(self.script), expected)


class ScriptTemplateTagTest(TestCase):
    def setUp(self):
        Script.objects.create(
            name='Head Script',
            code='<script>console.log("head");</script>',
            position='head',
            is_active=True,
            order=10
        )
        Script.objects.create(
            name='Body Script',
            code='<script>console.log("body");</script>',
            position='body_start',
            is_active=True,
            order=20
        )

    def test_render_scripts_tag(self):
        template = Template('{% load script_tags %}{% render_scripts "head" %}')
        rendered = template.render(Context())
        self.assertIn('Head Script', rendered)
        self.assertIn('console.log("head")', rendered)