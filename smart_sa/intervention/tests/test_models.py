from __future__ import unicode_literals

from django.test import TestCase
from django.utils.encoding import smart_str

from smart_sa.intervention.models import Activity
from smart_sa.intervention.models import Backup
from smart_sa.intervention.models import ClientSession
from smart_sa.intervention.models import Deployment
from smart_sa.intervention.models import Instruction
from smart_sa.intervention.models import Intervention
from smart_sa.intervention.models import Participant


class InterventionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(
            name="test intervention",
            intervention_id="1",
            general_instructions="this is for testing")

    def test_basics(self):
        self.assertEqual(smart_str(self.i), "test intervention")
        self.assertEqual(
            self.i.get_absolute_url().startswith("/intervention/"),
            True)

    def test_isolated_serialization(self):
        d = self.i.as_dict()
        # check the dict
        self.assertEqual(d['name'], "test intervention")
        self.assertEqual(d['intervention_id'], "1")
        self.assertEqual(d['general_instructions'], "this is for testing")
        i2 = Intervention.objects.create(name="test2",
                                         intervention_id="2",
                                         general_instructions="number 2")
        # check round-trip
        i2.from_dict(d)
        self.assertEqual(smart_str(i2), "test intervention")
        self.assertEqual(i2.intervention_id, "1")
        self.assertEqual(i2.general_instructions, "this is for testing")


class ClientSessionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(
            name="test intervention",
            intervention_id="1",
            general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(
            intervention=self.i,
            short_title="Test Session 1",
            long_title="Test Session 1 Long Title",
            introductory_copy="Introductory Copy Here",
            defaulter=False)

    def test_basics(self):
        self.assertEqual(self.cs.intervention, self.i)
        self.assertEqual(smart_str(self.cs), "Test Session 1")
        self.assertEqual(self.cs.get_absolute_url().startswith("/session/"),
                         True)
        self.assertEqual(self.cs.index(), 1)

    def test_isolated_serialization(self):
        d = self.cs.as_dict()
        self.assertEqual(d['short_title'], "Test Session 1")
        self.assertEqual(d['long_title'], "Test Session 1 Long Title")
        self.assertEqual(d['introductory_copy'], "Introductory Copy Here")
        self.assertEqual(d['defaulter'], False)
        # try round-tripping
        cs2 = ClientSession.objects.create(
            intervention=self.i,
            short_title="Test Session 2",
            long_title="Test Session 2 Long Title",
            introductory_copy="Introductory Copy 2 Here",
            defaulter=True)
        cs2.from_dict(d)
        self.assertEqual(smart_str(cs2), "Test Session 1")
        self.assertEqual(cs2.long_title, "Test Session 1 Long Title")
        self.assertEqual(cs2.introductory_copy, "Introductory Copy Here")
        self.assertEqual(cs2.defaulter, False)
        # we didn't delete self.cs, so this one should appear as second
        self.assertEqual(cs2.index(), 2)


class ActivityModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(
            name="test intervention",
            intervention_id="1",
            general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(
            intervention=self.i,
            short_title="Test Session 1",
            long_title="Test Session 1 Long Title",
            introductory_copy="Introductory Copy Here",
            defaulter=False)
        self.activity = Activity.objects.create(
            clientsession=self.cs,
            short_title="Activity 1",
            long_title="Activity 1 Long Title",
            objective_copy="Objective Copy for Activity 1 Here",
            collect_notes=False,
            collect_buddy_name=False,
            collect_referral_info=False,
            collect_reasons_for_returning=False)

    def test_basics(self):
        self.assertEqual(smart_str(self.activity), "Activity 1")
        self.assertEqual(
            self.activity.get_absolute_url().startswith("/activity/"),
            True)
        self.assertEqual(self.activity.index(), 1)

    def test_isolated_serialization(self):
        d = self.activity.as_dict()
        self.assertEqual(d['short_title'], "Activity 1")
        self.assertEqual(d['long_title'], "Activity 1 Long Title")
        self.assertEqual(d['objective_copy'],
                         "Objective Copy for Activity 1 Here")
        self.assertEqual(d['collect_notes'], False)
        self.assertEqual(d['collect_buddy_name'], False)
        self.assertEqual(d['collect_referral_info'], False)
        self.assertEqual(d['collect_reasons_for_returning'], False)
        # try round-tripping
        a2 = Activity.objects.create(
            clientsession=self.cs,
            short_title="Activity 2",
            long_title="Activity 2 Long Title",
            objective_copy="Objective Copy for Activity 2 Here",
            collect_notes=True,
            collect_buddy_name=True,
            collect_referral_info=True,
            collect_reasons_for_returning=True)
        a2.from_dict(d)
        self.assertEqual(smart_str(a2), "Activity 1")
        self.assertEqual(a2.long_title, "Activity 1 Long Title")
        self.assertEqual(a2.objective_copy,
                         "Objective Copy for Activity 1 Here")
        self.assertEqual(a2.collect_notes, False)
        self.assertEqual(a2.collect_buddy_name, False)
        self.assertEqual(a2.collect_referral_info, False)
        self.assertEqual(a2.collect_reasons_for_returning, False)


class InstructionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(
            name="test intervention",
            intervention_id="1",
            general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(
            intervention=self.i,
            short_title="Test Session 1",
            long_title="Test Session 1 Long Title",
            introductory_copy="Introductory Copy Here",
            defaulter=False)
        self.activity = Activity.objects.create(
            clientsession=self.cs,
            short_title="Activity 1",
            long_title="Activity 1 Long Title",
            objective_copy="Objective Copy for Activity 1 Here",
            collect_notes=False,
            collect_buddy_name=False,
            collect_referral_info=False,
            collect_reasons_for_returning=False)
        self.instruction = Instruction.objects.create(
            activity=self.activity,
            title="Instruction 1",
            style="do",
            instruction_text="Instruction Text for Instruction 1",
            help_copy="Help Copy for Instruction 1",
            notes="Notes for Instruction 1")

    def test_basics(self):
        self.assertEqual(self.instruction.index(), 1)

    def test_isolated_serialization(self):
        d = self.instruction.as_dict()
        self.assertEqual(d['title'], "Instruction 1")
        self.assertEqual(d['style'], "do")
        self.assertEqual(d['instruction_text'],
                         "Instruction Text for Instruction 1")
        self.assertEqual(d['help_copy'], "Help Copy for Instruction 1")
        self.assertEqual(d['notes'], "Notes for Instruction 1")
        # try round-tripping
        i2 = Instruction.objects.create(
            activity=self.activity,
            title="Instruction 2",
            style="say",
            instruction_text="Instruction Text for Instruction 2",
            help_copy="Help Copy for Instruction 2",
            notes="Notes for Instruction 2")
        i2.from_dict(d)
        self.assertEqual(i2.title, "Instruction 1")
        self.assertEqual(i2.style, "do")
        self.assertEqual(i2.instruction_text,
                         "Instruction Text for Instruction 1")
        self.assertEqual(i2.help_copy, "Help Copy for Instruction 1")
        self.assertEqual(i2.notes, "Notes for Instruction 1")


class FullSerializationTest(TestCase):
    fixtures = ["full_testdb.json"]

    def test_intervention_serialization(self):
        i = Intervention.objects.all()[0]
        d = i.as_dict()
        i2 = Intervention.objects.create(name="i2")
        i2.from_dict(d)

        self.assertEqual(i.clientsession_set.count(),
                         i2.clientsession_set.count())
        for idx in range(i.clientsession_set.count()):
            self.assertEqual(smart_str(i.get_session_by_index(idx + 1)),
                             smart_str(i2.get_session_by_index(idx + 1)))
            s1 = i.get_session_by_index(idx + 1)
            s2 = i2.get_session_by_index(idx + 1)

            self.assertEqual(smart_str(s1.next()), smart_str(s2.next()))

            for aidx in range(s1.activity_set.count()):
                a1 = s1.get_activity_by_index(idx + 1)
                a2 = s2.get_activity_by_index(idx + 1)
                self.assertEqual(smart_str(a1), smart_str(a2))
                self.assertEqual(smart_str(a1.next()), smart_str(a2.next()))
                self.assertEqual(smart_str(a1.prev()), smart_str(a2.prev()))
                self.assertEqual(
                    smart_str(a1.index()), smart_str(a2.index()))
                self.assertEqual(smart_str(a1.last_gamepage()),
                                 smart_str(a2.last_gamepage()))
                self.assertEqual(smart_str(a1.variables()),
                                 smart_str(a2.variables()))

                a1.pages()
                a2.pages()

                # TODO: understand why .gamepage_set.count()
                # can be higher than len(.pages())
                for pidx in range(min(a1.gamepage_set.count(),
                                      len(a1.pages()))):
                    p1 = a1.gamepage_set.all()[pidx]
                    p2 = a2.gamepage_set.all()[pidx]
                    self.assertEqual(p1.index(), p2.index())
                    self.assertEqual(p1.page_name(), p2.page_name())
                    self.assertEqual(p1.prev_title(), p2.prev_title())
                    self.assertEqual(p1.next_title(), p2.next_title())
                    self.assertEqual(str(p1.variables()), str(p2.variables()))

                for iidx in range(a1.instruction_set.count()):
                    ii1 = a1.instruction_set.all()[iidx]
                    ii2 = a2.instruction_set.all()[iidx]
                    self.assertEqual(ii1.index(), ii2.index())

    def test_participant_serialization(self):
        for p in Participant.objects.all():
            d = p.to_json()
            p2, logs = Participant.from_json(d)
            for log in logs:
                self.assertEqual('info' in log, True)
            self.assertEqual(logs[0], {'info': 'participant created'})
            self.assertEqual(p.name, p2.name)
            self.assertEqual(p.display_name(), p2.display_name())


class GamePageModelTest(TestCase):
    pass


class DeploymentModelTest(TestCase):
    def test_online(self):
        d1 = Deployment.objects.create(name="CCNMTL")
        d2 = Deployment.objects.create(name="Town 2")
        self.assertEqual(d1.is_online(), True)
        self.assertEqual(d1.is_clinic(), False)
        self.assertEqual(d2.is_online(), False)
        self.assertEqual(d2.is_clinic(), True)


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(
            name="test intervention",
            intervention_id="1",
            general_instructions="this is for testing")

        self.cs = ClientSession.objects.create(
            intervention=self.i,
            short_title="Session 1",
            long_title="Session 1: Getting Started",
            introductory_copy="Introductory Copy Here",
            defaulter=False)

        self.activity = Activity.objects.create(
            clientsession=self.cs,
            short_title="Activity 1",
            long_title="Activity 1 Long Title",
            objective_copy="Objective Copy for Activity 1 Here",
            collect_notes=False,
            collect_buddy_name=False,
            collect_referral_info=False,
            collect_reasons_for_returning=False)

        self.p1, logs = Participant.from_json(
            {
                'name': 'Test Participant 1',
                'patient_id': 'test_patient_1',
                'id_number': '1',
                'status': False,
                'gender': 'F',
                'buddy_name': '',
                'clinical_notes': 'Hello World!',
                'initial_referral_notes': 'Sample notes.',
                'initial_referral_alcohol': 0,
                'initial_referral_drug_use': 0,
                'initial_referral_mental_health': 0,
                'initial_referral_other': 0,
                'defaulter': True,
                'defaulter_referral_notes': 'Defaulter referral notes',
                'defaulter_referral_alcohol': 0,
                'defaulter_referral_drugs': 0,
                'defaulter_referral_mental_health': 0,
                'defaulter_referral_other': 0,
                'reasons_for_returning': 'Reasons for returning notes',
                'counselor_notes': [],
                'session_progress': [],
                'activity_progress': [],
                'game_vars': [],
                u'session_visits': [
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 12:58:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 12:59:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:00:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:01:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:02:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:03:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:04:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:05:17.340000'},
                    {u'session': u'Session 1: Session 1: Getting Started',
                     u'timestamp': u'2013-02-12 13:06:54.064000'}],
                u'activity_visits': [
                    {u'activity': u'Session 1: Activity 1: Session Objectives',
                     u'timestamp': u'2013-02-12 12:58:26.466000'}]
            })

        self.p2, log = Participant.from_json({
            'name': 'Test Participant 2',
            'patient_id': 'test_patient_2',
            'id_number': '2',
            'status': False,
            'gender': 'F',
            'buddy_name': '',
            'clinical_notes': 'Hello World!',
            'initial_referral_notes': 'Sample notes.',
            'initial_referral_alcohol': 0,
            'initial_referral_drug_use': 0,
            'initial_referral_mental_health': 0,
            'initial_referral_other': 0,
            'defaulter': True,
            'defaulter_referral_notes': 'Defaulter referral notes',
            'defaulter_referral_alcohol': 0,
            'defaulter_referral_drugs': 0,
            'defaulter_referral_mental_health': 0,
            'defaulter_referral_other': 0,
            'reasons_for_returning': 'Reasons for returning notes',
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
                 u'timestamp': u'2013-02-12 12:58:26.466000'}],
            u'game_vars': [
                {u'pill_game': u'{"regular": {"pills": [{"color": "#FF0000", \
                "id": "pill_8913", "name": "Efaverinez EFV"}, \
                {"color": "#0000FF", "id": "pill_2044", \
                "name": "Tenofivir TNV"}, {"color": "#00FF00", \
                "id": "pill_9305", "name": "Lamudivine 3TC"}], \
                "day": {"selected": "06:00", "id": "day", \
                "views": [{"top": "105px", "pillId": "pill_8913", \
                "left": "116px"}, {"top": "105px", "pillId": "pill_2044", \
                "left": "62px"}, {"top": "135px", "pillId": "pill_9305", \
                "left": "62px"}]}, "night": {"selected": "na", \
                "id": "night", "views": []}}}'},
                {u'assessmentquiz': u'{"defaulter": {"audit": {"total": 7}, \
                "drugaudit": {"total": 0}, "kten": {"total": 27}}, \
                "regular": {"audit": {}, "kten": {"total": 18}}}'},
                {u'ssnmtree': u'{"defaulter": {"middle1-fruit": \
                {"disclosure": true, "support": true, "name": "person1"}, \
                "bottom1-fruit": {"disclosure": false, "support": false, \
                "name": "person2"}, "bottom2-fruit": {"disclosure": true, \
                "support": true, "name": "person3"}, "top2-fruit": \
                {"disclosure": false, "support": false, "name": "person4"}, \
                "middle4-fruit": {"disclosure": false, "support": true, \
                "name": "person5"}, "middle3-fruit": {"disclosure": true, \
                "support": true, "name": "person6"}}, "regular": \
                {"middle1-fruit": {"disclosure": true, "support": true, \
                "name": "person7"}, "bottom1-fruit": {"disclosure": false, \
                "support": false, "name": "person8"}, "bottom2-fruit": \
                {"disclosure": true, "support": false, "name": "person9"}, \
                "top2-fruit": {"disclosure": false, "support": false, "name": \
                "person10"}, "middle4-fruit": {"disclosure": false, \
                "support": true, "name": "person11"}, "middle3-fruit": \
                {"disclosure": true, "support": true, "name": ""}}}'},
                {u'lifegoals': u'{"regular": {"step4": "educate my self", \
                "step3": "see my kids grow", "step2": "get healtheir", \
                "goal": "buy a car"}}'},
                {u'problemsolving': u'{"defaulter": {"peopletellmenotto": \
                {"customtext": ""}, "forgetful": {"barriers": \
                "tirednesss.confusion", "finalPlan": "setphone as a \
                reminder.speak to dr", "proposals": "get a relative to \
                help you to remember.\\n\\ntreatment buddy,speaking to dr \
                \\n\\n", "archive": [{"barriers": "wheniam drunk \
                iforget to drink my arv`s", "finalPlan": "Before i go to \
                drink i will ask my daughter to remind me my meds when i \
                come backor wake me up if i fall asleep before my next \
                dose.", "proposals": "get a relative to help you to \
                remember."}], "customtext": ""}, "cantgettoclinic": \
                {"customtext": ""}, "angrynurse": {"customtext": ""}, \
                "nonsense": {"customtext": ""}, \
                "confused": {"customtext": ""}, \
                "otherpatients": {"customtext": ""}, \
                "other": {"customtext": ""}, "hopeless": {"customtext": ""}, \
                "notenoughfood": {"customtext": ""}, \
                "feelingill": {"customtext": ""}, \
                "alone": {"barriers": "", "finalPlan": "", "proposals": "", \
                "customtext": ""}, "treatment_fatigue": {"customtext": ""}, \
                "dontwantto": {"customtext": ""}, \
                "happy": {"customtext": ""}}}'}],
        })

    def test_patient_id(self):
        assert self.p1.patient_id == 'test_patient_1'

    def test_id_number(self):
        assert self.p1.id_number == '1'

    def test_gender(self):
        assert self.p1.gender == 'F'

    def test_relevant_timestamps(self):
        self.assertEqual(len(self.p1.relevant_timestamps(self.cs)), 10)

    def test_session_duration(self):
        self.assertEqual(self.p1.session_duration(self.cs), 8)

    def test_ll_session_durations(self):
        self.assertEqual(self.p1.all_session_durations(), [8])

    def test_ssnmtree_data(self):
        self.assertIsNone(self.p1.ssnmtree_data())
        self.assertIsNotNone(self.p2.ssnmtree_data())

    def test_get_pill_data(self):
        self.assertIsNone(self.p1.get_pill_data())
        self.assertIsNotNone(self.p2.get_pill_data())

    def test_get_pill_name(self):
        self.assertIsNone(self.p1.get_pill_name('foo'))
        self.assertIsNone(self.p1.get_pill_name('pill_8913'))
        self.assertIsNone(self.p2.get_pill_name('foo'))
        self.assertIsNotNone(self.p2.get_pill_name('pill_8913'))

    def test_get_day_pills(self):
        self.assertIsNone(self.p1.get_day_pills())
        self.assertIsNotNone(self.p2.get_day_pills())

    def test_get_day_pill_time(self):
        self.assertIsNone(self.p1.get_day_pill_time())
        self.assertIsNotNone(self.p2.get_day_pill_time())

    def test_get_night_pills(self):
        self.assertIsNone(self.p1.get_night_pills())
        self.assertIsNotNone(self.p2.get_night_pills())

    def test_get_night_pill_time(self):
        self.assertIsNone(self.p1.get_night_pill_time())
        self.assertIsNotNone(self.p2.get_night_pill_time())

    def test_assessmentquiz_data(self):
        self.assertIsNone(self.p1.assessmentquiz_data())
        self.assertIsNotNone(self.p2.assessmentquiz_data())

    def test_lifegoals_data(self):
        self.assertIsNone(self.p1.lifegoals_data())
        self.assertIsNotNone(self.p2.lifegoals_data())

    def test_assessmentquiz_scores(self):
        self.assertEqual(self.p2.mood_alcohol_drug_scores(),
                         [18, '', ''])

    def test_ssnmtree_count(self):
        self.assertIsNone(self.p1.ssnmtree_total())
        self.assertIsNone(self.p1.ssnmtree_total('defaulter'))
        self.assertEqual(len(self.p2.ssnmtree_total()), 6)
        self.assertEqual(len(self.p2.ssnmtree_total('defaulter')), 6)

    def test_ssnmtree_supporters(self):
        self.assertIsNone(self.p1.ssnmtree_supporters())
        self.assertIsNone(self.p1.ssnmtree_supporters('defaulter'))
        self.assertEqual(len(self.p2.ssnmtree_supporters()), 3)
        self.assertEqual(len(self.p2.ssnmtree_supporters('defaulter')), 4)

    def test_ssnmtree_confidants(self):
        self.assertIsNone(self.p1.ssnmtree_confidants())
        self.assertIsNone(self.p1.ssnmtree_confidants('defaulter'))
        self.assertEqual(len(self.p2.ssnmtree_confidants()), 3)
        self.assertEqual(len(self.p2.ssnmtree_confidants('defaulter')), 3)

    def test_ssnmtree_supporters_and_confidants(self):
        self.assertIsNone(self.p1.ssnmtree_supporters_and_confidants())
        self.assertIsNone(
            self.p1.ssnmtree_supporters_and_confidants('defaulter'))
        self.assertEqual(len(self.p2.ssnmtree_supporters_and_confidants()), 2)
        self.assertEqual(
            len(self.p2.ssnmtree_supporters_and_confidants('defaulter')), 3)

    def test_barriers(self):
        self.assertEqual(self.p1.barriers(), "")
        self.assertEqual(self.p2.barriers(), "")


class ParticipantSessionModelTest(TestCase):
    pass


class ParticipantActivityModelTest(TestCase):
    pass


class CounselorNoteModelTest(TestCase):
    pass


class ParticipantGameVarModelTest(TestCase):
    pass


class BackupModelTest(TestCase):
    def setUp(self):
        self.b = Backup.objects.create(deployment="Clinic",
                                       json_data="""{'foo':'bar'}""")

    def test_as_dict(self):
        d = self.b.as_dict()
        self.assertEqual(d['deployment'], self.b.deployment)
        self.assertEqual(d['json_data'], self.b.json_data)
