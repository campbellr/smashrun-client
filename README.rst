===============
smashrun-client
===============

.. image:: https://travis-ci.org/campbellr/smashrun-client.svg?branch=master
    :target: https://travis-ci.org/campbellr/smashrun-client


A Python client for the Smashrun_ API.

Install
=======

You can install the current development release using ``pip``::

    pip install --pre smashrun-client


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
    code = raw_input("Go to '%s' and authorize this application. Paste the provided code here:" % auth_url[0])
    client.fetch_token(code=code)


**NOTE:** The example above assumes that you are running Python 2.x. If You are using Python 3.x you can replace
``raw_input`` with ``input``.


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
