from smoketest import SmokeTest
from smart_sa.intervention.models import Activity


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Activity.objects.all().count()
        self.assertTrue(cnt > 0)
