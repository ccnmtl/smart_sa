from smoketest import SmokeTest
from models import Activity


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Activity.objects.all().count()
        self.assertTrue(cnt > 0)
