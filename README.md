django-evesde
=============

A Django app abstracting out the EVE Online Static Data Extract into a usable format.

Inspired by @gtaylor's ``django-eve-db``, the idea is to a useful Django application for the EVE SDE data, with some extra tools for common operations on the SDE.


License
=======

This code is licensed under the BSD 3-clause License, for further details refer to the ``LICENSE`` file


Installation
============

Install by running ``python setup.py install`` either within your virtualenv or as root for a system-wide installation.


Usage / Documentation
=====================

This project generates its documentation via ``Sphinx``, to create the documentation run ``make html`` in the ``docs`` directory.

Testing
=======

Our aim is to have the project as testable as possible. Our tests are ran via standard Django tests, which can be run from the ``example_project`` folder by using ``python manage.py test``.
