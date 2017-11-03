Flask-ShellPlus
===============

Flask shell command based on Flask-Script to enhance its shell.

It will automatically use your favorite Python REPL shell instead
of the default one. The order is BPython to ptiPython to IPython
to ptPython to Python.

**Deprecated!!!**
-----------------

原因：`《初探 Flask 命令行接口》 <https://blog.windrunner.me/python/web/flask-cli.html>`__

Since Flask 0.11 released with builtin CLI, you should use it instead,
and it is also very easy.

eg. You want to use ``IPython>=5.0`` to provide a friendly REPL, just
add a command:

.. code-block:: python

    import os
    import click
    from flask import Flask

    app = Flask(__name__)

    @app.cli.command()
    def shell_plus():
        from IPython import embed
        embed(user_ns={'app': app, os: 'os'})

Then run ``flask shell_plus`` as the document leads, you'll get a REPL
with ``app`` and ``os`` already imported.

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
