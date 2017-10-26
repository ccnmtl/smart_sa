import csv
from smart_sa.intervention.models import Backup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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


@login_required
def download(request):
    clinics = []
    for d in DEPLOYMENTS:
        try:
            clinics.append(ClinicData(d))
        except IndexError:
            # test fixtures don't have all the clinics data
            # dummied out. So we need to be able to skip some
            # for the unit tests
            pass
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clinicdata.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            'clinic/laptop',
            'patient id',
            'id number',
            'gender',
            'buddy?',
            'Defaulter?',
            'Defaulter-A',
            'Defaulter-D',
            'Defaulter-M',
            'Defaulter-O',
            '# completed sessions',
            '# incomplete sessions',
            '# completed activities',
            'most recent completed session',
            'most recently completed session\'s date',
            'any skipped activities up through end of most recent completed ' +
            'session (comma separated)',
            'session durations for completed sessions (comma separated)',
            'session durations for all sessions (comma separated)',
            'mood, alcohol, drug scores (comma separated)',
            'number of names on tree',
            'number of names on tree marked with support',
            'number of names of tree marked with status',
            'number of names on tree marked with both support and status',
            'initial referral alcohol',
            'initial referral drug use',
            'initial referral mental health',
            'initial referral other',
            'referral comments',
            'your arvs: names of pills entered',
            'Session durations for 4 and or 5',
            'reasons for returning',
            's4/5 mood, alcohol, drug scores (comma separated)',
            's4/5 your arvs: names of pills (comma separated)',
            's4/5 number of names on tree',
            'barriers selected (comma separated)',
            'barriers with plans (comma separated)',
        ]
    )
    for clinic in clinics:
        name = clinic.deployment
        for participant in clinic.participants():
            writer.writerow(
                [
                    name,
                    participant.patient_id(),
                    participant.id_number(),
                    participant.gender(),
                    participant.has_buddy(),
                    participant.is_defaulter(),
                    participant.defaulter_a(),
                    participant.defaulter_d(),
                    participant.defaulter_m(),
                    participant.defaulter_o(),
                    participant.num_completed_sessions(),
                    participant.num_incomplete_sessions(),
                    participant.num_completed_activities(),
                    participant.most_recently_completed_session(),
                    participant.most_recently_completed_session_date(),
                    participant.skipped_activities(),
                    participant.completed_session_durations(),
                    participant.all_session_durations(),
                    participant.mood_alcohol_drug_scores(),
                    participant.ssnmtree_total(),
                    participant.ssnmtree_supporters(),
                    participant.ssnmtree_confidants(),
                    participant.ssnmtree_supporters_and_confidants(),
                    participant.referral_a(),
                    participant.referral_d(),
                    participant.referral_m(),
                    participant.referral_o(),
                    participant.initial_referral_notes(),
                    participant.medication_list(),
                    participant.session_45_durations(),
                    participant.reasons_for_returning(),
                    participant.defaulter_mood_alcohol_drug_scores(),
                    participant.defaulter_medication_list(),
                    participant.defaulter_ssnmtree_total(),
                    participant.defaulter_barriers(),
                    participant.defaulter_barriers_with_plans(),
                ]
            )
    return response
