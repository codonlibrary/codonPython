codonPython package
===================

Submodules
----------

codonPython.age\_bands module
-----------------------------

.. automodule:: codonPython.age_bands
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.check\_consistent\_measures module
----------------------------------------------

.. automodule:: codonPython.check_consistent_measures
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.check\_consistent\_submissions module
-------------------------------------------------

.. automodule:: codonPython.check_consistent_submissions
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.check\_nat\_val module
----------------------------------

.. automodule:: codonPython.check_nat_val
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.check\_null module
------------------------------

.. automodule:: codonPython.check_null
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.dateValidator module
--------------------------------

.. automodule:: codonPython.dateValidator
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.file\_utils module
------------------------------

.. automodule:: codonPython.file_utils
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.mesh module
-----------------------
.. automodule:: codonPython.mesh
   :members:
   :imported-members:
   :no-undoc-members:
   :exclude-members: dataclass
   :show-inheritance:
   :member-order: bysource

Requirements
++++++++++++
Using the MESH API requires a valid API certificate issued by DIR (for live environments) or Platforms (for development/test environments).
Guidance on obtaining a certificate can be found `in the MESH guidance hub <https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/certificate-guidance>`_.
The module requires the certificate be in PEM format; the certificate enrolment tool produces a java keystore which the valid certificate can be extracted from if needs be.
Due to limitations inherited from the Requests library, the private key *must* be unencrypted.

The keystore will also contain root authority certificates; these should also be extracted and combined into a certificate bundle for use in confirming the identity of the endpoint being communicated with. This check *can* be disabled, but this is not recommended.

Finally, use of the MESH API requires the API secret key, which can be requested from Platforms.

Example usage
+++++++++++++
.. include:: example_usage/mesh.rst

codonPython.nhsd\_colours module
--------------------------------

.. automodule:: codonPython.nhsd_colours
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.nhsNumber module
----------------------------

.. automodule:: codonPython.nhsNumber
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.ODS_lookup module
-----------------------------

.. automodule:: codonPython.ODS_lookup
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.suppression module
------------------------------

.. automodule:: codonPython.suppression
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.tableFromSql module
-------------------------------

.. automodule:: codonPython.tableFromSql
   :members:
   :undoc-members:
   :show-inheritance:

codonPython.tolerance module
----------------------------

.. automodule:: codonPython.tolerance
   :members:
   :undoc-members:
   :show-inheritance:


Module contents
---------------

.. automodule:: codonPython
   :members:
   :undoc-members:
   :show-inheritance:
