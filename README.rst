Overview
------------
.. image:: https://circleci.com/gh/CtheSky/namecom.svg?style=svg
    :target: https://circleci.com/gh/CtheSky/namecom
.. image:: https://codecov.io/gh/CtheSky/namecom/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/CtheSky/namecom
.. image:: https://img.shields.io/badge/python-2.7%2B%2C%203.4%2B-brightgreen.svg
  :target: https://github.com/CtheSky/namecom

*namecom* is a python library for the v4 api of `name.com <https://www.name.com>`_, a domain name registrar.

Installation
------------

If you haven't already, start by installing it
with *pip*::

   pip install --upgrade pynamecom

Quick Start
-----------

Use `DnsApi` to create a dns record:

.. sourcecode:: python

    from namecom import Auth, DnsApi

    auth = Auth('username', 'access_token')
    api = DnsApi(domainName='example.org', auth=auth)

    result = api.create_record(host='test', type='A', answer='10.0.0.1')

Documentation
-------------
Read more about this project at `readthedocs <https://namecom.readthedocs.io/en/latest/>`_:

* `Overview <https://namecom.readthedocs.io/en/latest/#overview>`_
* `Installaton <https://namecom.readthedocs.io/en/latest/#installation>`_
* `Quick Start <https://namecom.readthedocs.io/en/latest/#quick-start>`_
* `More About API <https://namecom.readthedocs.io/en/latest/#more-about-api>`_
* `More References <https://namecom.readthedocs.io/en/latest/#more-references>`_
* `Usage Example <https://namecom.readthedocs.io/en/latest/#usage-example>`_
* `Hey, it's not Snake Case! <https://namecom.readthedocs.io/en/latest/#hey-it-s-not-snake-case>`_
