from django.test import TestCase
from smart_sa.dashboard.models import Participant


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
                u'session_visits': [
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 12:58:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:06:54.064000'}],
                u'activity_visits': [
                    {u'activity': u'Session 1: Activity 1: Session Objectives',
                     u'timestamp': u'2013-02-12 12:58:26.466000'},
                    {u'activity':
                     u'Session 1: Activity 2: Welcome to Masivukeni!',
                     u'timestamp': u'2013-02-12 12:59:26.745000'},
                    {u'activity': u'Session 1: Activity 3: Today',
                     u'timestamp': u'2013-02-12 12:59:40.317000'},
                    {u'activity': u'Session 1: Activity 4: Working Together',
                     u'timestamp': u'2013-02-12 13:00:07.367000'},
                    {u'activity': u'Session 1: Activity 5: What are ARVs',
                     u'timestamp': u'2013-02-12 13:00:19.270000'},
                    {u'activity':
                     u'Session 1: Activity 6: Getting to Know ARVs',
                     u'timestamp': u'2013-02-12 13:00:30.674000'},
                    {u'activity': u'Session 1: Activity 7: Taking ARVs',
                     u'timestamp': u'2013-02-12 13:00:46.991000'},
                    {u'activity': u'Session 1: Activity 7: Taking ARVs',
                     u'timestamp': u'2013-02-12 13:01:09.643000'},
                    {u'activity': u'Session 1: Activity 8: ARV Concerns',
                     u'timestamp': u'2013-02-12 13:01:53.338000'},
                    {u'activity': u'Session 1: Activity 9: How Are You?',
                     u'timestamp': u'2013-02-12 13:02:20.233000'},
                    {u'activity': u'Session 1: Activity 10: Mood Screen',
                     u'timestamp': u'2013-02-12 13:02:35.989000'},
                    {u'activity': u'Session 1: Activity 10: Mood Screen',
                     u'timestamp': u'2013-02-12 13:02:45.988000'},
                    {u'activity': u'Session 1: Activity 11: Alcohol Screen',
                     u'timestamp': u'2013-02-12 13:03:47.628000'},
                    {u'activity': u'Session 1: Activity 11: Alcohol Screen',
                     u'timestamp': u'2013-02-12 13:03:56.598000'},
                    {u'activity': u'Session 1: Activity 12: Drug Screen',
                     u'timestamp': u'2013-02-12 13:04:41.261000'},
                    {u'activity': u'Session 1: Activity 12: Drug Screen',
                     u'timestamp': u'2013-02-12 13:04:47.813000'},
                    {u'activity': u'Session 1: Activity 13: Treatment Support',
                     u'timestamp': u'2013-02-12 13:05:03.694000'},
                    {u'activity': u'Session 1: Activity 13: Treatment Support',
                     u'timestamp': u'2013-02-12 13:05:10.901000'},
                    {u'activity':
                     u'Session 1: Activity 14: Disclosure is Important',
                     u'timestamp': u'2013-02-12 13:05:31.571000'},
                    {u'activity': u'Session 1: Activity 15: Choosing a Buddy',
                     u'timestamp': u'2013-02-12 13:05:40.182000'},
                    {u'activity': u'Session 1: Activity 15: Choosing a Buddy',
                     u'timestamp': u'2013-02-12 13:05:49.808000'},
                    {u'activity':
                     u'Session 1: Activity 16: Next Steps with Buddy',
                     u'timestamp': u'2013-02-12 13:06:03.005000'},
                    {u'activity':
                     u'Session 1: Activity 17: Reasons to Stay Healthy',
                     u'timestamp': u'2013-02-12 13:06:14.206000'},
                    {u'activity':
                     u'Session 1: Activity 17: Reasons to Stay Healthy',
                     u'timestamp': u'2013-02-12 13:06:22.100000'},
                    {u'activity': u'Session 1: Activity 18: End Session',
                     u'timestamp': u'2013-02-12 13:06:32.364000'}],
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

    def test_most_recently_completed_session(self):
        self.assertEquals(self.p1.most_recently_completed_session(), None)

    def test_relevant_timestamps(self):
        self.assertEquals(len(self.p1.relevant_timestamps(1)), 27)

    def test_session_duration(self):
        self.assertEquals(self.p1.session_duration(1), 8)
