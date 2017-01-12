.. image:: https://img.shields.io/badge/Supported%20by-Clockwork-ffcc00.svg
    :alt: badge: Supported by Clockwork
    :align: right
    :target: https://www.clockwork.com/

kernel_cleanup
==============

Evaluate installed Linux kernel packages (``linux-headers``, ``linux-image``,
``linux-image-extra``) and purge any that are not the current version or the
newest version.


Cron Example
------------

``dpkg`` expects a more robust path::

    PATH=/usr/sbin:/usr/bin:/sbin:/bin
    @daily /usr/local/sbin/kernel_cleanup.py -q


Compatibility
-------------

.. image:: https://img.shields.io/travis/ClockworkNet/kernel_cleanup/master.svg
    :alt: badge: Travis CI master branch status
    :align: right
    :target: https://travis-ci.org/ClockworkNet/kernel_cleanup
Tested on:

- Ubuntu 10.04 LTS (Lucid Lynx)
- Ubuntu 12.04 LTS (Precise Pangolin)
- Ubuntu 14.04 LTS (Trusty Tahr)
- Ubuntu 16.04 LTS (Xenial Xerus)


Testing Quick Start
===================

1. Change directory into repository (into same directory as where this README
   resides).
2. Install virtual environment::

    mkvirtualenv --system-site-packages -a $(pwd) -r tests/requirements.txt \
        kernel_cleanup_test

   a. If installing requirements errors, update `pip`::

        pip install --upgrade pip

   b. Install requirements::

        pip install -r tests/requirements.txt

3. Run pytest::

    py.test

To test against alternate Python versions, it may be useful to create virtual
environments with an interpreter other than the one with which ``virtualenv``
was installed, e.g. for non-default python3::

    mkvirtualenv --system-site-packages -a $(pwd) -p $(which python3) \
        -r tests/requirements.txt kernel_cleanup_test3


License
-------

.. image:: https://img.shields.io/github/license/ClockworkNet/kernel_cleanup.svg
    :alt: badge: GitHub license (MIT)
    :align: right
    :target: `MIT License`_
- `<LICENSE>`_ (`MIT License`_)

.. _`MIT License`: http://www.opensource.org/licenses/MIT
