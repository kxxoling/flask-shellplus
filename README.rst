Flask-ShellPlus
===============

Flask shell command based on Flask-Script to enhance its shell.

It will automatically use your favorite Python REPL shell instead
of the default one. The order is BPython to ptiPython to IPython
to ptPython to Python.


Installation
------------

pip is suggested::

    pip install flask_shellplus


Usage
-----

Use it with Flask-Script:

.. code-block:: python

    from flask_shellplus import Shell

    def make_context():
        return dict(app=app, db=db, models=models)

    manager.add_command('shell', Shell(make_context=make_context))

Run this in your shell::

    python manage.py shell

Flask-ShellPlus will find the first available one in BPython, ptiPython,
IPython, ptPython, and Python.

Or you can manually define the preferred shell with flag ``--plain``,
``--bpython``, ``--ptipython``, ``--ipython`` or ``--ptpython`` just
like ``shell_plus`` in DjangoExtensions.

Enjoy it!


Links
-----

* `GitHub <https://github.com/kxxoling/flask-shellplus>`__
* `PyPI <https://pypi.python.org/pypi/Flask-ShellPlus>`__
* `Documentation <https://flask-shellplus.readthedocs.org/>`__
