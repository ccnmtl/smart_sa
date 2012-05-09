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
        a = Activity.objects.all()[0]
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

    def test_login_nonexistant_participant(self):
        resp = self.client.post('/set_participant/', {'name' : 'notapatient', 'id_number': 'foo'})
        self.assertEqual(resp.content,"no participant with that name")

    def test_login_inactive_participant(self):
        p = Participant.objects.get(name='test')
        p.status = False
        p.save()
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        self.assertEqual(resp.content,"this participant is marked as inactive")

    def test_login_participant_with_wrong_password(self):
        resp = self.client.post('/set_participant/', {'name' : 'test', 'id_number': 'wrong password'})
        self.assertEqual(resp.content,"id number does not match")

    def test_practice_mode(self):
         for i in Intervention.objects.all():
             resp = self.client.get("/practice/%d/" % i.id, follow=True)
             self.assertEqual("You are in Practice Mode. Changes will not be saved." in resp.content, True)
         s = ClientSession.objects.all()[0]
         resp = self.client.get(s.get_absolute_url())
         self.assertEqual("You are in Practice Mode. Changes will not be saved." in resp.content, True)
         a = s.activity_set.all()[0]
         resp = self.client.get(a.get_absolute_url())
         self.assertEqual("You are in Practice Mode. Changes will not be saved." in resp.content, True)

    def test_complete_session(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        for s in ClientSession.objects.all():
            resp = self.client.post(s.get_absolute_url() + "complete/")
            self.assertEqual(resp.status_code, 302)

    def test_complete_activity(self):
        resp = self.client.post('/set_participant/', {'name': 'test', 'id_number': 'test'})
        a = Activity.objects.all()[0]
        resp = self.client.post(a.get_absolute_url() + "complete/")
        self.assertEqual(resp.status_code, 302)

    # def test_save_game_state(self):
    #     pass

class InterventionAdminViewTest(TestCase):
    """ test functionality that needs an admin logged in"""

    fixtures = ["full_testdb.json"]

    def setUp(self):
        self.client = client.Client()
        self.client.login(username='testadmin',password='test')

    def test_set_deployment(self):
        resp = self.client.post("/set_deployment/",{"name" : "new clinic name"})
        resp = self.client.get("/")
        self.assertEqual("new clinic name" in resp.content, True)

    def test_manage_participants(self):
        resp = self.client.get("/manage/")
        self.assertEqual(resp.status_code, 200)

    # def test_add_participant(self):
    #     pass

    # def test_delete_participant(self):
    #     pass

    def test_edit_participant(self):
        t = Participant.objects.get(name="test")
        resp = self.client.get("/manage/participant/%d/edit/" % t.id)
        self.assertEqual(resp.status_code, 200)

    def test_view_participant(self):
        t = Participant.objects.get(name="test")
        resp = self.client.get("/manage/participant/%d/view/" % t.id)
        self.assertEqual(resp.status_code, 200)
        # check that it asks for password
        self.assertEqual("Please enter password" in resp.content, True)
        # make a POST request with password to actually see the page
        resp = self.client.post("/manage/participant/%d/view/" % t.id, {'password' : "test"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual("Please enter password" in resp.content, False)

    # def test_edit_counselor(self):
    #     pass

    # def test_add_counselor(self):
    #     pass

    def test_participant_data_download(self):
        resp = self.client.get("/manage/report/download/")
        self.assertEqual(resp.status_code,200)

    # def test_download_backup(self):
    #     pass

    # def test_restore_participants(self):
    #     pass

    # def test_upload_participant_data(self):
    #     pass

    # def test_update_intervention_content(self):
    #     pass

    # def test_intervention_admin(self):
    #     pass

    # def test_activity_admin(self):
    #     pass

    # def test_gamepage_admin(self):
    #     pass

    # def test_zip_download(self):
    #     pass
