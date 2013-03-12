from smart_sa.intervention.models import Backup
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from smart_sa.dashboard.models import DEPLOYMENTS
from smart_sa.dashboard.models import ClinicData


@render_to("dashboard/index.html")
@login_required
def index(request):
    missing_deployments = False
    for deployment in DEPLOYMENTS:
        if Backup.objects.filter(
            deployment=deployment
        ).count() < 1:
            missing_deployments = True
    if not missing_deployments:
        clinics = [ClinicData(d) for d in DEPLOYMENTS]
        return dict(clinics=clinics)
    else:
        return dict(missing_deployments=missing_deployments)
