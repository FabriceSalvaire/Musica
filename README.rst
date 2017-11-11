.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |MusicaUrl|
   |MusicaHomePage|_
   |MusicaDoc|_
   |Musica@github|_
   |Musica@readthedocs|_
   |Musica@readthedocs-badge|
   |Musica@pypi|_

.. https://musica.fabrice-salvaire.fr
.. https://fabricesalvaire.github.io/Musica

.. |MusicaUrl| replace:: https://musica.fabrice-salvaire.fr

.. |MusicaHomePage| replace:: Musica Home Page
.. _MusicaHomePage: https://musica.fabrice-salvaire.fr

.. |Musica@readthedocs-badge| image:: https://readthedocs.org/projects/musica/badge/?version=latest
   :target: http://musica.readthedocs.org/en/latest

.. |Musica@github| replace:: https://github.com/FabriceSalvaire/Musica
.. .. _Musica@github: https://github.com/FabriceSalvaire/Musica

.. |Musica@pypi| replace:: https://pypi.python.org/pypi/musica-toolkit
.. .. _Musica@pypi: https://pypi.python.org/pypi/musica-toolkit

.. |Pypi Version| image:: https://img.shields.io/pypi/v/musica-toolkit.svg
   :target: https://pypi.python.org/pypi/musica-toolkit
   :alt: Musica last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/musica-toolkit.svg
   :target: https://pypi.python.org/pypi/Musica
   :alt: Musica license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/musica-toolkit.svg
   :target: https://pypi.python.org/pypi/musica-toolkit
   :alt: Musica python version

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/Musica.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/Musica
   :alt: Musica build status @travis-ci.org

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star

.. End
.. -*- Mode: rst -*-

.. |IPython| replace:: IPython
.. _IPython: http://ipython.org

.. |Numpy| replace:: Numpy
.. _Numpy: http://www.numpy.org

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Python| replace:: Python
.. _Python: http://python.org

.. End

===============
 Musica Tookit
===============

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/Musica/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/Musica/tree/devel>`_

Overview
========

What is the Musica Toolkit ?
----------------------------

Musica is a free and open source computational music toolkit written in |Python|_ covering several
topics from music theory, audio analysis to high quality figure generation.

Where is the Documentation ?
----------------------------

The documentation is available on the |MusicaHomePage|_.

What are the main features ?
----------------------------

.. -*- Mode: rst -*-

* Music Theory : temperament, pitch, interval, scale
* Audio Analysis

  * Spectrum analysis, e.g. Harmonic Power Spectrum to find the pitch

* Database using YAML format

  * Instrument database covering usual orchestrations, e.g. classic and jazz music
  * Tuning database for string instruments

* Localisation

  * handle English and Latin convention
  * translation of music therms using `gettext`

* Score Format

  * read/write `MusiXML <http://www.musicxml.com/>`_, automatically generated from XML schema (thanks to `PyXB <http://pyxb.sourceforge.net>`_)

* High Quality Figures : piano keyboard, fretboard etc.

.. http://www.codesynthesis.com/products/xsd/

How to install it ?
-------------------

Look at the `installation <https://musica.fabrice-salvaire.fr/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. -*- Mode: rst -*-


.. no title here

V0 2017-10-01
-------------

Started project

.. End
