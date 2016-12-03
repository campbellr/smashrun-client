import os
import logging
import datetime

import requests
from unittest2 import TestCase, SkipTest

from smashrun import Smashrun

client_id = os.environ.get("SMASHRUN_CLIENT_ID")
client_secret = os.environ.get("SMASHRUN_CLIENT_SECRET")
refresh_token = os.environ.get("SMASHRUN_REFRESH_TOKEN")

if os.environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)


class TestSmashrun(TestCase):

    """Tests for the smashrun client.

    Note that these tests are *not* unit tests and actually run against the
    live Smashrun API, so be nice and don't repeatedly run them a ridiculous
    amount.

    """

    @classmethod
    def setUpClass(cls):
        if not all((client_id, client_secret, refresh_token)):
            raise SkipTest("Missing SMASHRUN_REFRESH_TOKEN, "
                           "SMASHRUN_CLIENT_ID, and SMASHRUN_CLIENT_SECRET "
                           "environment variables")

    def setUp(self):
        self.client = Smashrun(client_id=client_id,
                               client_secret=client_secret,
                               redirect_uri='http://localhost')
        self.client.refresh_token(refresh_token=refresh_token)

    def test_get_activities(self):
        activities = list(self.client.get_activities())
        self.assertNotEqual(activities, [])  # small chance this will fail...

    def test_get_activities_style(self):
        for style in ('summary', 'briefs', 'ids'):
            activities = self.client.get_activities(count=2, style='ids')
            activity = next(activities)
            self.assertIsInstance(activity, int)

    def test_get_activities_invalid_style(self):
        with self.assertRaises(requests.HTTPError):
            list(self.client.get_activities(style='foobar'))

    def test_get_activities_limit(self):
        activities = list(self.client.get_activities(style='ids', limit=3))
        self.assertEqual(len(activities), 3)

    def test_get_activities_since(self):
        one_month_ago = (datetime.datetime.now() -
                         datetime.timedelta(days=30))
        # TODO: it would be easier to have a test for this if each date field
        # was converted to a datetime...
        list(self.client.get_activities(since=one_month_ago))

    def test_get_activity(self):
        activities = self.client.get_activities()
        activity = next(activities)
        id_num = activity['activityId']
        fetched_activity = self.client.get_activity(id_num)
        self.assertEqual(activity['activityId'],
                         fetched_activity['activityId'])
        self.assertIn('recordingValues', fetched_activity)

    def test_get_badges(self):
        # if it doesn't raise an exception, that's good enough for me
        self.client.get_badges()

    def test_get_current_weight(self):
        self.client.get_current_weight()

    def test_get_weight_history(self):
        self.client.get_weight_history()

    def test_get_stats(self):
        self.client.get_stats()

    def test_get_stats_year(self):
        self.client.get_stats(year=2014)

    def test_get_stats_year_month(self):
        self.client.get_stats(year=2015, month=2)

    def test_get_stats_month_and_no_year(self):
        with self.assertRaises(ValueError):
            self.client.get_stats(month=1)

    def test_get_auth_url(self):
        url = self.client.get_auth_url()[0]
        self.assertIn('client_id', url)
        self.assertIn('client_secret', url)
        self.assertIn('redirect_uri', url)

    def test_get_userinfo(self):
        r = self.client.get_userinfo()
        self.assertIn('id', r)
