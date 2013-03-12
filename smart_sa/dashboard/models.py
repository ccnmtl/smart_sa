from smart_sa.intervention.models import Backup
from simplejson import loads
import dateutil.parser
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


def extract_session_number(session):
    return int(session['session'][8])


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

    def initial_referral_notes(self):
        return self.data.get('initial_referral_notes', '')

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

    def most_recently_completed_session_date(self):
        if self.num_completed_sessions() < 1:
            return None
        sessions = self.completed_sessions()
        sessions.sort(key=lambda s: s['session'])
        most_recent_session = extract_session_number(sessions[-1])
        # we don't actually have any way of knowing when
        # a session was completed, so we have to settle
        # for the last time it was visited
        return self.last_session_visit(most_recent_session)

    def last_session_visit(self, session_number):
        if 'session_visits' not in self.data:
            return None
        if 'activity_visits' not in self.data:
            return None
        timestamps = self.relevant_timestamps(session_number)
        timestamps.sort()
        if len(timestamps) > 0:
            return dateutil.parser.parse(timestamps[-1])
        else:
            return None

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

        # obviously, it would be more efficient to make this into
        # a dictionary first instead of looping over the list
        # over and over again, but so far it doesn't seem to actually
        # be a bottleneck
        for ap in self.completed_activities():
            if ap['activity'].startswith(
                    "Session %d: Activity %d:" % (session, activity)):
                return True
        else:
            return False

    def session_duration(self, session):
        """ approximate number of minutes participant spent
        on a given session

        since we just care about a total, not whether it was all
        continuous or not, we can "cheat" and take advantage
        of the fact that the front end logs every minute and just
        count the number of relevant visit logs.

        That can go wrong if they are flying through and visiting
        more than one page a minute; we'd get a higher number from
        the count than the actual total time. So we compare our
        count to the absolute difference between the earliest and
        latest timestamps we have and take the min.

        This can still be inaccurate if they flew through parts
        and then had gaps (computer shut off, logged out, etc)
        in other parts. So a proper run through merging timestamps
        that are less than a minute apart into runs would be ideal.
        But this should get us pretty close without too much craziness.
        Since the logging is pretty rough at best, this is probably
        good enough, at least for now.
        """
        timestamps = self.relevant_timestamps(session)
        simple_count = len(timestamps)

        if simple_count < 2:
            # zero or 1 timestamps logged, so this is as
            # accurate as we can get
            return simple_count

        # otherwise, double check against absolute time interval
        timestamps.sort()
        earliest = dateutil.parser.parse(timestamps[0])
        latest = dateutil.parser.parse(timestamps[-1])
        delta = latest - earliest
        if (delta.seconds / 60.0) < simple_count:
            return delta.seconds / 60
        else:
            return simple_count

    def relevant_timestamps(self, session):
        """ all the timestamps for a session and activities in that session """
        return (self.session_timestamps(session)
                + self.session_activity_timestamps(session))

    def session_timestamps(self, session):
        if 'session_visits' not in self.data:
            return []
        return [sv['timestamp'] for sv in self.data['session_visits']
                if sv['session'].startswith("Session %d:" % session)]

    def session_activity_timestamps(self, session):
        if 'activity_visits' not in self.data:
            return []
        return [sv['timestamp'] for sv in self.data['activity_visits']
                if sv['activity'].startswith("Session %d:" % session)]

    def completed_session_durations(self):
        if self.num_completed_sessions() < 1:
            return ""
        durations = []
        for s in range(1, self.max_completed_session_number() + 1):
            durations.append(self.session_duration(s))
        return ",".join([str(d) for d in durations])

    def session_45_durations(self):
        """ explicitly calculate durations for sessions 4 and 5 """
        if self.num_completed_sessions() < 1:
            return ""
        durations = []
        for s in [4, 5]:
            durations.append(self.session_duration(s))
        return ",".join([str(d) for d in durations])

    def game_vars(self, name):
        for d in self.data[u'game_vars']:
            if name in d:
                return loads(d[name])
        return {}

    def ssnmtree_data(self):
        return self.game_vars(u'ssnmtree')

    def assessmentquiz_data(self):
        return self.game_vars(u'assessmentquiz')

    def lifegoals_data(self):
        return self.game_vars(u'lifegoals')
