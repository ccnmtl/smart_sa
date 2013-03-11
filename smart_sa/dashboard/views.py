from annoying.decorators import render_to
from smart_sa.intervention.models import Backup
from django.contrib.auth.decorators import login_required
from simplejson import loads
import pprint

# list of the deployments that we want to view data for
# for each of these, we'll just pull up the most recent
# data upload that we can find. We'll call them "clinics"
# in other parts of the code though, as that's closer
# to how the researchers view the data (and 'deployment'
# was originally chosen as the terminology as it included
# both clinics and the main website)
DEPLOYMENTS = [
    'Mzamomhle 1',
    'Mzamomhle 2',
    'Town II 1',
    'Town 2',
]

# how many activities, per session we know exist
# so we can go through and see which ones a participant
# may have skipped
EXPECTED_ACTIVITIES = [
    18,
    13,
    22,
    22,  # defaulter 1
    17,  # defaulter 2
]


class ClinicData(object):
    """ a more useful class for dealing with clinic data
    via parsed json instead of the json string """
    def __init__(self, deployment):
        self.deployment = deployment
        self.backup = Backup.objects.filter(
            deployment=deployment
        ).order_by("-created")[0]
        self.created = self.backup.created
        self.data = loads(self.backup.json_data)

    def pprint(self):
        return pprint.pformat(self.data['participants'])

    def keys(self):
        return self.data.keys()

    def num_participants(self):
        return len([p for p in self.data['participants'] if p['patient_id']])

    def participants(self):
        return [Participant(p)
                for p in self.data['participants'] if p['patient_id']]


def strip_session_title(session):
    """ session titles are kind of ugly, like:
        Session 2: Session 2: Learning About HIV Treatment
    we let them put the number in there twice and didn't catch it
    before it launched. For the dashboard page, just "Session 2"
    should be identifying enough """
    return session['session'][:9]


class Participant(object):
    """ more useful object than the raw dict form """
    def __init__(self, data):
        self.data = data

    def patient_id(self):
        return self.data['patient_id']

    def pprint(self):
        return pprint.pformat(self.data)

    def id_number(self):
        return self.data['id_number']

    def gender(self):
        return self.data['gender']

    def has_buddy(self):
        return self.data['buddy_name'] != u''

    def initial_referral_status(self):
        return "%s|%s|%s|%s" % (
            ["-", "X"][int(self.data['initial_referral_alcohol'])],
            ["-", "X"][int(self.data['initial_referral_drug_use'])],
            ["-", "X"][int(self.data['initial_referral_mental_health'])],
            ["-", "X"][int(self.data['initial_referral_other'])],
        )

    def defaulter_status(self):
        if not self.data['defaulter']:
            return "False"
        else:
            return "True: %s|%s|%s|%s" % (
                ["-", "X"][int(self.data['defaulter_referral_alcohol'])],
                ["-", "X"][int(self.data['defaulter_referral_drugs'])],
                ["-", "X"][int(self.data['defaulter_referral_mental_health'])],
                ["-", "X"][int(self.data['defaulter_referral_other'])],
            )

    def counselor_notes(self):
        return [cn for cn in self.data.get('counselor_notes', [])
                if cn['notes'] != u'']

    def has_counselor_notes(self):
        return len([cn for cn in self.data['counselor_notes']
                    if cn['notes'] != u'']) > 0

    def completed_sessions(self):
        return [sp for sp in self.data['session_progress']
                if sp['status'] == 'complete']

    def num_completed_sessions(self):
        return len(self.completed_sessions())

    def num_incomplete_sessions(self):
        return len([sp for sp in self.data['session_progress']
                    if sp['status'] == 'incomplete'])

    def completed_activities(self):
        return [ap for ap in self.data['activity_progress']
                if ap['status'] == 'complete']

    def num_completed_activities(self):
        return len(self.completed_activities())

    def num_activity_visits(self):
        if 'activity_visits' in self.data:
            return len(self.data['activity_visits'])
        else:
            return 0

    def num_session_visits(self):
        if 'session_visits' in self.data:
            return len(self.data['session_visits'])
        else:
            return 0

    def session_visits(self):
        return self.data['session_visits']

    def activity_visits(self):
        return self.data['activity_visits']

    def clinical_notes(self):
        return self.data.get('clinical_notes', '')

    def most_recently_completed_session(self):
        if self.num_completed_sessions() < 1:
            return None
        sessions = self.completed_sessions()
        sessions.sort(key=lambda s: s['session'])
        return strip_session_title(sessions[-1])

    def max_completed_session_number(self):
        return int(self.most_recently_completed_session()[-1])

    def reasons_for_returning(self):
        return self.data.get('reasons_for_returning', '')

    def skipped_activities(self):
        """ any skipped activities up through end of most
        recent completed session """
        if self.num_completed_sessions() < 1:
            return ""
        all_skipped = []
        for s in range(0, self.max_completed_session_number()):
            expected = EXPECTED_ACTIVITIES[s]
            for a in range(expected):
                if not self.is_activity_completed(s + 1, a + 1):
                    all_skipped.append(
                        "Session %d: Activity %d" % (s + 1, a + 1))
        return ",".join(all_skipped)

    def is_activity_completed(self, session, activity):
        """ did this user complete the specified session/activity """
        for ap in self.completed_activities():
            if ap['activity'].startswith(
                    "Session %d: Activity %d:" % (session, activity)):
                return True
        else:
            return False


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
