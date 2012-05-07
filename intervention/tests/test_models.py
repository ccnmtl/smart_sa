from django.test import TestCase
from smart_sa.intervention.models import Activity
from smart_sa.intervention.models import ClientSession
from smart_sa.intervention.models import Deployment
from smart_sa.intervention.models import Instruction
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
        # check the dict
        self.assertEqual(d['name'],"test intervention")
        self.assertEqual(d['intervention_id'],"1")
        self.assertEqual(d['general_instructions'],"this is for testing")
        i2 = Intervention.objects.create(name="test2",
                                         intervention_id="2",
                                         general_instructions="number 2")
        # check round-trip
        i2.from_dict(d)
        self.assertEqual(unicode(i2),"test intervention")
        self.assertEqual(i2.intervention_id,"1")
        self.assertEqual(i2.general_instructions,"this is for testing")

class ClientSessionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(name="test intervention",
                                             intervention_id="1",
                                             general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(intervention = self.i,
                                               short_title = "Test Session 1",
                                               long_title = "Test Session 1 Long Title",
                                               introductory_copy = "Introductory Copy Here",
                                               defaulter = False)

    def test_basics(self):
        self.assertEqual(self.cs.intervention,self.i)
        self.assertEqual(unicode(self.cs),"Test Session 1")
        self.assertEqual(self.cs.get_absolute_url().startswith("/session/"),True)
        self.assertEqual(self.cs.index(),1)

    def test_isolated_serialization(self):
        d = self.cs.as_dict()
        self.assertEqual(d['short_title'],"Test Session 1")
        self.assertEqual(d['long_title'],"Test Session 1 Long Title")
        self.assertEqual(d['introductory_copy'],"Introductory Copy Here")
        self.assertEqual(d['defaulter'],False)
        # try round-tripping
        cs2 = ClientSession.objects.create(intervention = self.i,
                                           short_title = "Test Session 2",
                                           long_title = "Test Session 2 Long Title",
                                           introductory_copy = "Introductory Copy 2 Here",
                                           defaulter = True)
        cs2.from_dict(d)
        self.assertEqual(unicode(cs2),"Test Session 1")
        self.assertEqual(cs2.long_title,"Test Session 1 Long Title")
        self.assertEqual(cs2.introductory_copy,"Introductory Copy Here")
        self.assertEqual(cs2.defaulter,False)
        # we didn't delete self.cs, so this one should appear as second
        self.assertEqual(cs2.index(),2)

class ActivityModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(name="test intervention",
                                             intervention_id="1",
                                             general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(intervention = self.i,
                                               short_title = "Test Session 1",
                                               long_title = "Test Session 1 Long Title",
                                               introductory_copy = "Introductory Copy Here",
                                               defaulter = False)
        self.activity = Activity.objects.create(clientsession = self.cs,
                                                short_title = "Activity 1",
                                                long_title = "Activity 1 Long Title",
                                                objective_copy = "Objective Copy for Activity 1 Here",
                                                collect_notes = False,
                                                collect_buddy_name = False,
                                                collect_referral_info = False,
                                                collect_reasons_for_returning = False)

    def test_basics(self):
        self.assertEqual(unicode(self.activity),"Activity 1")
        self.assertEqual(self.activity.get_absolute_url().startswith("/activity/"),True)
        self.assertEqual(self.activity.index(),1)

    def test_isolated_serialization(self):
        d = self.activity.as_dict()
        self.assertEqual(d['short_title'],"Activity 1")
        self.assertEqual(d['long_title'],"Activity 1 Long Title")
        self.assertEqual(d['objective_copy'],"Objective Copy for Activity 1 Here")
        self.assertEqual(d['collect_notes'],False)
        self.assertEqual(d['collect_buddy_name'],False)
        self.assertEqual(d['collect_referral_info'],False)
        self.assertEqual(d['collect_reasons_for_returning'],False)
        # try round-tripping
        a2 = Activity.objects.create(clientsession = self.cs,
                                     short_title = "Activity 2",
                                     long_title = "Activity 2 Long Title",
                                     objective_copy = "Objective Copy for Activity 2 Here",
                                     collect_notes = True,
                                     collect_buddy_name = True,
                                     collect_referral_info = True,
                                     collect_reasons_for_returning = True)
        a2.from_dict(d)
        self.assertEqual(unicode(a2),"Activity 1")
        self.assertEqual(a2.long_title,"Activity 1 Long Title")
        self.assertEqual(a2.objective_copy,"Objective Copy for Activity 1 Here")
        self.assertEqual(a2.collect_notes,False)
        self.assertEqual(a2.collect_buddy_name,False)
        self.assertEqual(a2.collect_referral_info,False)
        self.assertEqual(a2.collect_reasons_for_returning,False)


class InstructionModelTest(TestCase):
    def setUp(self):
        self.i = Intervention.objects.create(name="test intervention",
                                             intervention_id="1",
                                             general_instructions="this is for testing")
        self.cs = ClientSession.objects.create(intervention = self.i,
                                               short_title = "Test Session 1",
                                               long_title = "Test Session 1 Long Title",
                                               introductory_copy = "Introductory Copy Here",
                                               defaulter = False)
        self.activity = Activity.objects.create(clientsession = self.cs,
                                                short_title = "Activity 1",
                                                long_title = "Activity 1 Long Title",
                                                objective_copy = "Objective Copy for Activity 1 Here",
                                                collect_notes = False,
                                                collect_buddy_name = False,
                                                collect_referral_info = False,
                                                collect_reasons_for_returning = False)

        self.instruction = Instruction.objects.create(activity = self.activity,
                                                      title = "Instruction 1",
                                                      style = "do",
                                                      instruction_text = "Instruction Text for Instruction 1",
                                                      help_copy = "Help Copy for Instruction 1",
                                                      notes = "Notes for Instruction 1")
        
    def test_basics(self):
        self.assertEqual(self.instruction.index(),1)

    def test_isolated_serialization(self):
        d = self.instruction.as_dict()
        self.assertEqual(d['title'],"Instruction 1")
        self.assertEqual(d['style'],"do")
        self.assertEqual(d['instruction_text'],"Instruction Text for Instruction 1")
        self.assertEqual(d['help_copy'],"Help Copy for Instruction 1")
        self.assertEqual(d['notes'],"Notes for Instruction 1")
        # try round-tripping
        i2 = Instruction.objects.create(activity = self.activity,
                                        title = "Instruction 2",
                                        style = "say",
                                        instruction_text = "Instruction Text for Instruction 2",
                                        help_copy = "Help Copy for Instruction 2",
                                        notes = "Notes for Instruction 2")
        i2.from_dict(d)
        self.assertEqual(i2.title,"Instruction 1")
        self.assertEqual(i2.style,"do")
        self.assertEqual(i2.instruction_text,"Instruction Text for Instruction 1")
        self.assertEqual(i2.help_copy,"Help Copy for Instruction 1")
        self.assertEqual(i2.notes,"Notes for Instruction 1")

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
