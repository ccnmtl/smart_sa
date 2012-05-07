from django.test import TestCase
from smart_sa.intervention.models import Deployment
from smart_sa.intervention.models import Intervention

class InterventionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(name="test intervention",
                                             intervention_id="1",
                                             general_instructions="this is for testing")
    def test_basics(self):
        self.assertEqual(unicode(self.i),"test intervention")
        self.assertEqual(self.i.get_absolute_url().startswith("/intervention/"),True)

    def test_isolated_serialization(self):
        d = self.i.as_dict()
        self.assertEqual(d['name'],"test intervention")
        self.assertEqual(d['intervention_id'],"1")
        self.assertEqual(d['general_instructions'],"this is for testing")
        i2 = Intervention.objects.create(name="test2",
                                         intervention_id="2",
                                         general_instructions="number 2")

        i2.from_dict(d)
        self.assertEqual(unicode(i2),"test intervention")
        self.assertEqual(i2.intervention_id,"1")
        self.assertEqual(i2.general_instructions,"this is for testing")

class ClientSessionModelTest(TestCase):
    pass

class ActivityModelTest(TestCase):
    pass

class InstructionModelTest(TestCase):
    pass

class GamePageModelTest(TestCase):
    pass

class DeploymentModelTest(TestCase):
    def test_online(self):
        d1 = Deployment.objects.create(name="CCNMTL")
        d2 = Deployment.objects.create(name="Town 2")
        self.assertEqual(d1.is_online(),True)
        self.assertEqual(d1.is_clinic(),False)
        self.assertEqual(d2.is_online(),False)
        self.assertEqual(d2.is_clinic(),True)

class ParticipantModelTest(TestCase):
    pass

class ParticipantSessionModelTest(TestCase):
    pass

class ParticipantActivityModelTest(TestCase):
    pass

class CounselorNoteModelTest(TestCase):
    pass

class ParticipantGameVarModelTest(TestCase):
    pass

class BackupModelTest(TestCase):
    pass
