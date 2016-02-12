from smart_sa.intervention.models import Backup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from smart_sa.dashboard.models import DEPLOYMENTS
from smart_sa.dashboard.models import ClinicData


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
        return render(request, "dashboard/index.html",
                      dict(clinics=clinics))
    else:
        return render(request, "dashboard/index.html",
                      dict(missing_deployments=missing_deployments))
