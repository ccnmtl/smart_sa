from django.test import TestCase
from smart_sa.intervention.models import Deployment

class InterventionModelTest(TestCase):
    def test_as_dict(self):
        self.assertEqual(200, 200)

class DeploymentModelTest(TestCase):
    def test_online(self):
        d1 = Deployment.objects.create(name="CCNMTL")
        d2 = Deployment.objects.create(name="Town 2")
        self.assertEqual(d1.is_online(),True)
        self.assertEqual(d1.is_clinic(),False)
        self.assertEqual(d2.is_online(),False)
        self.assertEqual(d2.is_clinic(),True)
