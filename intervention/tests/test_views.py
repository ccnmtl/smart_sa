from django.test import TestCase
from django.test import client
from smart_sa.intervention.models import Intervention, ClientSession, Activity, Participant


class IndexViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

class InterventionViewTest(TestCase):

    fixtures = ["full_testdb.json"]
    def setUp(self):
        self.client = client.Client()
        self.client.login(username='testcounselor',password='test')

    def test_logged_out_index(self):
        self.client.logout()
        resp = self.client.get('/intervention/')
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='testcounselor',password='test')

    def test_logged_in_index(self):
        resp = self.client.get('/intervention/')
        self.assertEqual(resp.status_code, 200)

    def test_log_in_participant(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'}, follow=True)
        (url,status) = resp.redirect_chain[0]
        self.assertEqual("/intervention/" in url, True)

    def test_intervention_pages(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        for i in Intervention.objects.all():
            resp = self.client.get(i.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

    def test_session_pages(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        for s in ClientSession.objects.all():
            resp = self.client.get(s.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

            
    def test_activity_pages(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        for a in Activity.objects.all():
            resp = self.client.get(a.get_absolute_url())
            self.assertEqual(resp.status_code, 200)
