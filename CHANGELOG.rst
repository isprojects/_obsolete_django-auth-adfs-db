=========
Changelog
=========

0.3.0 (2021-03-31)
==================

* Updated compatibility with django-auth-adfs 1.6.x:

    * added setting ``JWT_LEEWAY``
    * added setting ``CREATE_NEW_USERS``
    * added setting ``CUSTOM_FAILED_RESPONSE_VIEW``

    All added settings have the default value from the upstream library and are static
    (for the time being).

* Fixed Azure AD integration:

    * added setting ``CLIENT_SECRET``, configurable in the admin
    * ensure that the ``SERVER`` setting is properly injected
    * updated help texts in admin models to better reflect Azure UI as of March 2021

* Migrated from Travis to Github Actions
* Support Python 3.6 through 3.9 (3.8 and 3.9 are added)
* Support Django 2.2 and 3.1 (3.0 support has been dropped)
