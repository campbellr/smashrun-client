""" This module contains main user-facing Smashrun interface.

"""
import json
import time

from requests_oauthlib import OAuth2Session

auth_url = "https://secure.smashrun.com/oauth2/authenticate"
token_url = "https://secure.smashrun.com/oauth2/token"


class Smashrun(object):
    def __init__(self, client_id=None, client_secret=None, client=None,
                 auto_refresh_url=None, auto_refresh_kwargs=None, scope=None,
                 redirect_uri=None, token=None, state=None, token_updater=None,
                 **kwargs):
        self.session = OAuth2Session(
            client_id=client_id,
            client=client,
            auto_refresh_url=token_url,
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            state=state,
            token_updater=token_updater,
            **kwargs
        )
        self.client_secret = client_secret
        self.base_url = "https://api.smashrun.com/v1"

    @property
    def client_id(self):
        return self.session.client_id

    def get_auth_url(self):
        return self.session.authorization_url(auth_url, client_secret=self.client_secret)

    def fetch_token(self, **kwargs):
        """Fetch a new token using the supplied code.

        :param str code: A previously obtained auth code.

        """
        if 'client_secret' not in kwargs:
            kwargs.update(client_secret=self.client_secret)
        return self.session.fetch_token(token_url, **kwargs)

    def refresh_token(self, **kwargs):
        """Refresh the authentication token.

        :param str refresh_token: The refresh token to use. May be empty if
                                  retrieved with ``fetch_token``.

        """
        if 'client_secret' not in kwargs:
            kwargs.update(client_secret=self.client_secret)
        if 'client_id' not in kwargs:
            kwargs.update(client_id=self.client_id)
        return self.session.refresh_token(token_url, **kwargs)

    def get_activity(self, id_num):
        """Return the activity with the given id.

        Note that this contains more detailed information than returned
        by `get_activities`.

        """
        url = self._build_url('my', 'activities', id_num)
        return self._json(url)

    def get_activities(self, count=10, since=None, style='summary'):
        """Iterate over all activities, from newest to oldest.

        :param count: The number of results to retrieve per page.
        :param since: Return only activities since this date.
        :param style: The type of records to return. May be one of
                      'summary', 'brief', or 'ids'.

        """
        if style not in ('summary', 'brief', 'ids'):
            raise ValueError("invalid value for 'style'")
        params = {}
        if since:
            params.update(fromDate=to_timestamp(since))
        parts = ['my', 'activities', 'search']
        if style != 'summary':
            parts.append(style)
        url = self._build_url(*parts)
        # TODO: return an Activity (or ActivitySummary?) class that can do
        # things like convert date and time fields to proper datetime objects
        return self._iter(url, count, **params)

    def get_badges(self):
        """Return all badges the user has earned."""
        url = self._build_url('my', 'badges')
        return self._json(url)

    def get_stats(self, year=None, month=None):
        """Return stats for the given year and month."""
        parts = ['my', 'stats']
        if month and not year:
            raise ValueError("month cannot be specified without year")
        if year:
            parts.append(year)
        if month:
            parts.append(year)
        url = self._build_url(*parts)
        return self._json(url)

    def get_current_weight(self):
        """Return the most recent weight recording."""
        url = self._build_url('my', 'body', 'weight', 'latest')
        return self._json(url)

    def get_weight_history(self):
        """Return all weight recordings."""
        url = self._build_url('my', 'body', 'weight')
        return self._json(url)

    def get_userinfo(self):
        """Return information about the current user."""
        url = self._build_url('my', 'userinfo')
        return self._json(url)

    def create_weight(self, weight, date=None):
        """Submit a new weight record.

        :param weight: The weight, in kilograms.
        :param date: The date the weight was recorded. If not
                     specified, the current date will be used.

        """
        if not date.is_aware():
            raise ValueError("provided date is not timezone aware")
        url = self._build_url('my', 'body', 'weight')
        data = {'weightInKilograms': weight}
        if date:
            data.update(date=date.isoformat())
        r = self.session.post(url, data=json.dumps(data))
        r.raise_for_status()
        return r

    def create_activity(self, data):
        """Create a new activity (run).

        :param data: The data representing the activity you want to upload.
                     May be either JSON, GPX, or TCX.

        """
        url = self._build_url('my', 'activities')
        if isinstance(data, dict):
            data = json.dumps(data)
        r = self.session.post(url, data=data)
        r.raise_for_status()
        return r

    def _iter(self, url, count, cls=None, **kwargs):
        page = 0
        while True:
            kwargs.update(count=count, page=page)
            r = self.session.get(url, params=kwargs)
            r.raise_for_status()
            data = r.json()
            if not data:
                break
            for d in data:
                if cls:
                    yield cls(d)
                else:
                    yield d
            page += 1

    def _build_url(self, *args, **kwargs):
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        return "/".join(parts)

    def _json(self, url):
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


def to_timestamp(dt):
    """Convert a datetime object to a unix timestamp (UTC)."""
    return int(time.mktime(dt.timetuple()))


def is_aware(d):
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None
