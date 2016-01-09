===============
Flask-ShellPlus
===============

Flask-ShellPlus is a Flask extension aimed to enhance your debugging with Flask apps.
It's heavily affected by `Django-Extentions <https://django-extensions.readthedocs.org/>`_
``shell_plus`` module but focused on Flask and on the top of `Flask-Script
<https://flask-script.readthedocs.org/>`_.

Flask-ShellPlus supports BPython, IPython, ptPython and ptiPython now, and also with
Jupyter notebook on the way.


Installation
------------

You could easily install it via pip::

    pip install flask_shellplus



Quick start
-----------

This should be used with Flask-Script:

.. code-block:: python

    from flask_shellplus import Shell

    def make_context():
        return dict(app=app, db=db, models=models)

    manager.add_command('shell', Shell(make_context=make_context))


Then run this in your shell::

    python manage.py shell


Flask-ShellPlus will find the first available one in BPython, ptiPython,
IPython, ptPython, and Python.

Or you can manually define the preferred shell with flag ``--plain``,
``--bpython``, ``--ptipython``, ``--ipython`` or ``--ptpython`` just
like ``shell_plus`` in DjangoExtensions.

.. note::

    If you want to use Flask ShellPlus with IPython, IPython 3.0 or newer is needed.


Configure
---------

Flask ShellPlus also provide configures as Django-Extensions do.
By now, ``SHELL_PLUS_PRE_IMPORTS`` and ``SHELL_PLUS_POST_IMPORTS`` is supported,
and others in progress:

.. code-block:: python

    SHELL_PLUS_PRE_IMPORTS = (          # SHELL_PLUS_POST_IMPORTS is similar to this
        ('module.submodule1', ('class1', 'function2')),
        ('module.submodule2', 'function3'),
        ('module.submodule3', '*'),
        'module.submodule4'
    )


You could define these arguments in your Flask application's configure file,
and they will be automate imported before and after ``make_context`` runs.


Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

