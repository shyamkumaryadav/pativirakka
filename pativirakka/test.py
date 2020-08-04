from django.test import TestCase


class ViewTest(TestCase):

    def test_is_false(self):
        self.assertFalse(False)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
