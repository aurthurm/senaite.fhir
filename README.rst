FHIR API for SENAITE LIMS
=========================


About
-----

This SENAITE.FHIR is a FHIR API for `SENAITE LIMS`_, that allows to exchange
SENAITE electronic health records (EHRs) with other systems, using RESTful
services and JSON as the format for data representation.

Installation
------------

Add *senaite.fhir* in the eggs section of your buildout:

.. code-block:: ini

  eggs =
      senaite.lims
      senaite.patient
      senaite.fhir

and run *bin/buildout*.


Documentation
-------------

* https://fhir.senaite.org


License
-------

**SENAITE.FHIR** Copyright (C) 2026 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2`_ as published by the
Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.


.. Links

.. _SENAITE LIMS: https://www.senaite.com
.. _GNU General Public License version 2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
