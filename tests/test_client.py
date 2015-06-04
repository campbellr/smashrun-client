import os
import logging

from unittest2 import TestCase, SkipTest, skip

from smashrun import Smashrun

client_id = os.environ.get("SMASHRUN_CLIENT_ID")
client_secret = os.environ.get("SMASHRUN_CLIENT_SECRET")
refresh_token = os.environ.get("SMASHRUN_REFRESH_TOKEN")

logging.basicConfig(level=logging.DEBUG)

class TestSmashrun(TestCase):

    @classmethod
    def setUpClass(cls):
        if not all((client_id, client_secret, refresh_token)):
            raise SkipTest("Missing SMASHRUN_REFRESH_TOKEN, "
                           "SMASHRUN_CLIENT_ID, and SMASHRUN_CLIENT_SECRET "
                           "environment variables")

    def setUp(self):
        self.client = Smashrun(client_id=client_id,
                               client_secret=client_secret)
        self.client.refresh_token(refresh_token=refresh_token)

    def test_get_activities(self):
        activities = list(self.client.get_activities())
        self.assertNotEqual(activities, [])  # small chance this will fail...

    def test_get_activity(self):
        activities = self.client.get_activities()
        activity = next(activities)
        id_num = activity['activityId']
        fetched_activity = self.client.get_activity(id_num)
        self.assertEqual(activity['activityId'],
                         fetched_activity['activityId'])
        self.assertIn('recordingValues', fetched_activity)
