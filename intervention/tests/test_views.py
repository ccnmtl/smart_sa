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

    def test_clear_participant(self):
        # make sure we have one logged in
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        # now clear it
        resp = self.client.get('/clear_participant/', follow=True)
        # try hitting a session page and make sure we get redirected
        s = ClientSession.objects.all()[0]
        resp = self.client.get(s.get_absolute_url(), follow=True)
        (url,status) = resp.redirect_chain[0]
        self.assertEqual(status,302)
        self.assertEqual("/set_participant/" in url, True)

    # def test_login_nonexistant_participant(self):
    #     pass

    # def test_login_inactive_participant(self):
    #     pass

    # def test_login_participant_with_wrong_password(self):
    #     pass

    # def test_set_deployment(self):
    #     pass

    # def test_practice_mode(self):
    #     pass

    # def test_manage_participants(self):
    #     pass

    # def test_add_participant(self):
    #     pass

    # def test_delete_participant(self):
    #     pass

    # def test_edit_participant(self):
    #     pass

    # def test_edit_counselor(self):
    #     pass

    # def test_view_participant(self):
    #     pass

    # def test_add_counselor(self):
    #     pass

    # def test_participant_data_download(self):
    #     pass

    # def test_download_backup(self):
    #     pass

    # def test_restore_participants(self):
    #     pass

    # def test_upload_participant_data(self):
    #     pass

    # def test_update_intervention_content(self):
    #     pass

    # def test_complete_session(self):
    #     pass

    # def test_complete_activity(self):
    #     pass

    # def test_save_game_state(self):
    #     pass

    # def test_intervention_admin(self):
    #     pass

    # def test_activity_admin(self):
    #     pass

    # def test_gamepage_admin(self):
    #     pass

    # def test_zip_download(self):
    #     pass
