Welcome to django-auth-adfs-db's documentation!
===============================================

:Version: 0.1.0
:Source: https://github.com/isprojects/django-auth-adfs-db
:Keywords: ADFS, Django, database, authentication backend
:PythonVersion: 3.7

|build-status| |coverage|

|python-versions| |django-versions| |pypi-version|

A database-backed django-auth-adfs settings class

.. contents::

.. section-numbering::

Features
========

* Thin layer on top of `django-auth-adfs`_
* SAAS ready: store ADFS configuration in a database singleton
* Quick toggle to enable/disable ADFS based auth
* Hooks into Django's auth machinery

Django-auth-adfs-db provides a setting class reading out the dynamic ADFS
configuration. This moves the ADFS configuration from deploy-time to run-time,
and SAAS clients can configure their ADFS integration themselves. No more
server reloads of deployment environment variable changes needed!

Installation
============

Requirements
------------

* Python 3.6 or higher
* setuptools 30.3.0 or higher
* Django 2.1 or higher
* PostgreSQL (with jsonb field)

Install
-------

.. code-block:: bash

    pip install django-auth-adfs-db

This will also install the ``django-auth-adfs`` and ``django-solo`` packages.

Django settings
---------------

Make sure the following libraries are added to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "django_auth_adfs"
        "django_auth_adfs_db"
        "solo",
        ...
    ]

Add ``django_auth_adfs_db.backends.AdfsAuthCodeBackend`` to
``AUTHENTICATION_BACKENDS``.

Ensure that ``LOGIN_URL`` and ``LOGIN_REDIRECT_URL`` are configured. You can
set:

.. code-block:: python

    LOGIN_URL = reverse_lazy("django_auth_adfs:login")
    LOGIN_REDIRECT_URL = "/"

if you wish to make ADFS your primary auth login.

Set the ``AUTH_ADFS`` config class:

.. code-block:: python

    AUTH_ADFS = {"SETTINGS_CLASS": "django_auth_adfs_db.settings.Settings"}

or a subclass thereof.

Finally, register the URLs in your root config with:

.. code-block:: python

    urlpatterns += [path("oauth2/", include("django_auth_adfs.urls")),]

ADFS login URL on admin login
-----------------------------

Template: ``admin/login.html``

.. code-block:: django

    {% extends "admin/login.html" %}
    {% load solo_tags i18n %}


    {% block content %}
    {{ block.super }}

    {% get_solo 'openzaak_auth.ADFSConfig' as adfs_config %}
    {% if adfs_config.enabled %}
    <div class="submit-row">
        <a href="{% url 'django_auth_adfs:login' %}">{% trans "Login with ADFS" %}</a>
    </div>
    {% endif %}
    {% endblock %}

Usage
=====

You can now configure the ADFS settings in the Django admin.

Please follow the ``django-auth-adfs`` documentation for advanced usage.


.. |build-status| image:: https://travis-ci.org/isprojects/django-auth-adfs-db.svg?branch=develop
    :target: https://travis-ci.org/isprojects/django-auth-adfs-db

.. |coverage| image:: https://codecov.io/gh/isprojects/django-auth-adfs-db/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/isprojects/django-auth-adfs-db
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-auth-adfs-db.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-auth-adfs-db.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-auth-adfs-db.svg
    :target: https://pypi.org/project/django-auth-adfs-db/

.. _django-auth-adfs: https://pypi.org/project/django-auth-adfs/
