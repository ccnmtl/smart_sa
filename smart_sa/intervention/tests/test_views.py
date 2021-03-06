from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.test import client
from smart_sa.intervention.models import (
    Intervention, ClientSession, Activity, Participant)


class IndexViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


class InterventionViewTest(TestCase):

    fixtures = ["full_testdb.json"]

    def setUp(self):
        self.client = client.Client()
        u = User.objects.get(username='testcounselor')
        u.set_password('test')
        u.save()
        self.client.login(username='testcounselor', password='test')

    def test_logged_out_index(self):
        self.client.logout()
        resp = self.client.get('/intervention/')
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='testcounselor', password='test')

    def test_logged_in_index(self):
        resp = self.client.get('/intervention/')
        self.assertEqual(resp.status_code, 200)

    def test_log_in_participant(self):
        resp = self.client.post(
            '/set_participant/',
            {'name': 'test', 'id_number': 'test'}, follow=True)
        (url, status) = resp.redirect_chain[0]
        self.assertEqual("/intervention/" in url, True)

    def test_intervention_pages(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        for i in Intervention.objects.all():
            resp = self.client.get(i.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

    def test_session_pages(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        for s in ClientSession.objects.all():
            resp = self.client.get(s.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

    def test_activity_pages(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        a = Activity.objects.all()[0]
        resp = self.client.get(a.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_intervention_report(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        p = Participant.objects.first()
        resp = self.client.get(reverse('intervention-report', args=[p.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_clear_participant(self):
        # make sure we have one logged in
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        # now clear it
        resp = self.client.get('/clear_participant/', follow=True)
        # try hitting a session page and make sure we get redirected
        s = ClientSession.objects.all()[0]
        resp = self.client.get(s.get_absolute_url(), follow=True)
        (url, status) = resp.redirect_chain[0]
        self.assertEqual(status, 302)
        self.assertEqual("/set_participant/" in url, True)

    def test_login_nonexistant_participant(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'notapatient', 'id_number': 'foo'})
        self.assertContains(resp, "no participant with that name")

    def test_login_inactive_participant(self):
        p = Participant.objects.get(name='test')
        p.status = False
        p.save()
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        self.assertContains(resp, "this participant is marked as inactive")

    def test_login_participant_with_wrong_password(self):
        resp = self.client.post(
            '/set_participant/',
            {'name': 'test', 'id_number': 'wrong password'})
        self.assertContains(resp, "id number does not match")

    def test_complete_session(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        for s in ClientSession.objects.all():
            resp = self.client.post(s.get_absolute_url() + "complete/")
            self.assertEqual(resp.status_code, 302)

    def test_complete_activity(self):
        resp = self.client.post(
            '/set_participant/', {'name': 'test', 'id_number': 'test'})
        a = Activity.objects.all()[0]
        resp = self.client.post(a.get_absolute_url() + "complete/")
        self.assertEqual(resp.status_code, 302)


class InterventionAdminViewTest(TestCase):
    """ test functionality that needs an admin logged in"""

    fixtures = ["full_testdb.json"]

    def setUp(self):
        self.client = client.Client()
        u = User.objects.get(username='testadmin')
        u.set_password('test')
        u.save()
        self.client.login(username='testadmin', password='test')

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
        self.assertContains(resp, "Please enter password")
        # make a POST request with password to actually see the page
        resp = self.client.post(
            "/manage/participant/%d/view/" % t.id, {'password': "test"})
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Please enter password")

    # def test_edit_counselor(self):
    #     pass

    # def test_add_counselor(self):
    #     pass

    def test_participant_data_download(self):
        resp = self.client.get("/manage/report/download/")
        self.assertEqual(resp.status_code, 200)

    # def test_restore_participants(self):
    #     pass

    # def test_update_intervention_content(self):
    #     pass

    def test_intervention_admin(self):
        i = Intervention.objects.all()[0]
        resp = self.client.get("/intervention_admin/%d/" % i.id)
        self.assertEqual(resp.status_code, 200)

    def test_session_admin(self):
        s = ClientSession.objects.all()[0]
        resp = self.client.get("/intervention_admin/session/%d/" % s.id)
        self.assertEqual(resp.status_code, 200)

    def test_activity_admin(self):
        a = Activity.objects.all()[0]
        resp = self.client.get("/intervention_admin/activity/%d/" % a.id)
        self.assertEqual(resp.status_code, 200)

    # def test_gamepage_admin(self):
    #     pass

    def test_zip_download(self):
        resp = self.client.get("/intervention_admin/zip_download/")
        self.assertEqual(resp.status_code, 200)

    def test_list_uploads(self):
        resp = self.client.get("/intervention_admin/list_uploads/")
        self.assertEqual(resp.status_code, 200)
