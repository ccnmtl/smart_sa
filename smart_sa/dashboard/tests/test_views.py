from django.contrib.auth.models import User
from django.test import TestCase


class IndexViewTest(TestCase):
    fixtures = ["full_testdb.json"]

    def setUp(self):
        u = User.objects.get(username='testcounselor')
        u.set_password('test')
        u.save()
        self.client.login(username='testcounselor', password='test')

    def test_index(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)

    def test_download(self):
        resp = self.client.get('/dashboard/download/')
        self.assertEqual(resp.status_code, 200)
