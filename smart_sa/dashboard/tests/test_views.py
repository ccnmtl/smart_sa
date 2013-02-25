from django.test import TestCase
from django.test import client
from smart_sa.dashboard.views import Participant


class IndexViewTest(TestCase):
    fixtures = ["full_testdb.json"]

    def setUp(self):
        self.client.login(username='testcounselor', password='test')

    def test_index(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)


class ParticipantTest(TestCase):
    def setUp(self):
        self.p1 = Participant(
            {
                'patient_id': 'test_patient_1',
                'id_number': '1',
                'gender': 'F',
                'buddy_name': '',
                'initial_referral_alcohol': 0,
                'initial_referral_drug_use': 0,
                'initial_referral_mental_health': 0,
                'initial_referral_other': 0,
                'defaulter': True,
                'defaulter_referral_alcohol': 0,
                'defaulter_referral_drugs': 0,
                'defaulter_referral_mental_health': 0,
                'defaulter_referral_other': 0,
                'counselor_notes': [],
                'session_progress': [],
                'activity_progress': [],
            })

    def test_patient_id(self):
        assert self.p1.patient_id() == 'test_patient_1'

    def test_id_number(self):
        assert self.p1.id_number() == '1'

    def test_gender(self):
        assert self.p1.gender() == 'F'

    def test_has_buddy(self):
        assert not self.p1.has_buddy()

    def test_initial_referral_status(self):
        assert self.p1.initial_referral_status() == "-|-|-|-"

    def test_defaulter_status(self):
        self.assertEquals(self.p1.defaulter_status(), "True: -|-|-|-")

    def test_has_counselor_notes(self):
        self.assertEquals(self.p1.has_counselor_notes(), False)

    def test_num_completed_sessions(self):
        self.assertEquals(self.p1.num_completed_sessions(), 0)

    def test_num_incomplete_sessions(self):
        self.assertEquals(self.p1.num_incomplete_sessions(), 0)

    def test_num_completed_activities(self):
        self.assertEquals(self.p1.num_completed_activities(), 0)
