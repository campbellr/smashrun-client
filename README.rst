===============
smashrun-client
===============

A Python client for the Smashrun_ API.

Install
=======

This package isn't on PyPi yet, so the easiest way to install is directly
from the git repository::

    $ pip install git+git://github.com/campbellr/smashrun-client.git

Usage
=====

Authentication
--------------

Using an existing refresh token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = Smashrun(client_id='my_client_id', client_secret='my_secret')
    client.refresh_token(refresh_token='my_refresh_token')

Requesting a token
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # use urn:ietf:wg:oauth:2.0:oob for applications that aren't a web app
    client = Smashrun(client_id='my_client_id',
                      redirect_uri='urn:ietf:wg:oauth:2.0:auto')
    auth_url = client.get_auth_url()
    code = input("Go to '%s' and authorize this application. Paste the provided code here:" % auth_url)
    client.fetch_token(code=code)


Fetching activities
-------------------

Use ``Smashrun.get_activities`` to get a list of activities (summaries):

.. code-block:: python

    activities = client.get_activities()  # returns an iterator that handles paginating through the API
    for activity in activities:
        print activity['startDateTimeLocal']


Fetch a specific activity
-------------------------

Use ``Smashrun.get_activity`` to get a specific activity:

.. code-block:: python

    activity = client.get_activity(1234)
    print activity['recordingKeys']


For more details on what you can do, see `the code`_ and the `Smashrun API`_


Contributing
============

Contributions are greatly appreciated! Feel free to submit a pull request, or file
an issue in our `issue tracker`_.

.. _Smashrun: https://smashrun.com
.. _issue tracker: https://github.com/campbellr/smashrun-client/issues
.. _the code: https://github.com/campbellr/smashrun-client/blob/master/smashrun/client.py
.. _Smashrun API: https://api.smashrun.com/
