.. _exception-reference-label:

Exception Reference
===================

:class:`~namecom.exceptions.NamecomError` is the base exception class,
all its subclass has fixed `status_code` and
`message`.

:meth:`~namecom.exceptions.make_exception` is used by api
to throw errors, it accepts a response, parse the `status_code` and `message` and map
the error to a specific exception class.

.. automodule:: namecom.exceptions
  :members:
