from django.test import TestCase

class IndexViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

class InterventionViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/intervention/')
        self.assertEqual(resp.status_code, 302)

