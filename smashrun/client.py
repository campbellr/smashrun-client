""" This module contains main user-facing Smashrun interface.

"""

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
        return self.session.authorization_url(auth_url)

    def fetch_token(self, **kwargs):
        if 'client_secret' not in kwargs:
            kwargs.update(client_secret=self.client_secret)
        return self.session.fetch_token(token_url, **kwargs)

    def refresh_token(self, **kwargs):
        if 'client_secret' not in kwargs:
            kwargs.update(client_secret=self.client_secret)
        if 'client_id' not in kwargs:
            kwargs.update(client_id=self.client_id)
        return self.session.refresh_token(token_url, **kwargs)

    def get_activity(self, id_num):
        url = self._build_url('my', 'activities', id_num)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_activities(self, count=10):
        url = self._build_url('my', 'activities', 'search')
        # TODO: return an Activity (or ActivitySummary?) class that can do
        # things like convert date and time fields to proper datetime objects
        return self._iter(url, count)

    def _iter(self, url, count, cls=None):
        page = 0
        while True:
            r = self.session.get(url, params={'count': count, 'page': page})
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
