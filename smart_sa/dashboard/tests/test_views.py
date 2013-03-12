from django.test import TestCase


class IndexViewTest(TestCase):
    fixtures = ["full_testdb.json"]

    def setUp(self):
        self.client.login(username='testcounselor', password='test')

    def test_index(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
