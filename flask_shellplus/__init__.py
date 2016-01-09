#!/usr/bin/env python
# coding: utf-8
import os
import sys
import logging
from collections import OrderedDict

import six
from flask import current_app
from flask.ext.script import Command, Option

from .utils import import_items


__version__ = '0.0.2'


class Shell(Command):
    """
    Runs a Python shell inside Flask application context.
    :param banner: banner appearing at top of shell when started.
                   Not available when you choose IPython or ptiPython to use.
    :param context: context used in you shell namespace. By default
                    contains the current app.
    :param make_context: should be a callable object. Used to update shell context.
    """

    help = description = 'Runs a Python shell inside Flask application context.'

    def __init__(self, banner='', context=None, make_context=None):
        self.banner = banner

        self.context = context or {}
        if make_context is not None:
            self.context.update(make_context())
        if not self.context:
            self.context = self.context or dict(app=current_app)

    def get_options(self):
        return (
            Option('--plain', action='store_true', dest='plain',
                        help='Tells Flask to use plain Python, not BPython nor IPython.'),
            Option('--bpython', action='store_true', dest='bpython',
                        help='Tells Flask to use BPython, not IPython.'),
            Option('--ptpython', action='store_true', dest='ptpython',
                        help='Tells Flask to use PTPython, not IPython.'),
            Option('--ptipython', action='store_true', dest='ptipython',
                        help='Tells Flask to use PT-IPython, not IPython.'),
            Option('--ipython', action='store_true', dest='ipython',
                        help='Tells Flask to use IPython, not BPython.'),
            Option('--notebook', action='store_true', dest='notebook',
                        help='Tells Flask to use IPython Notebook.'),
            Option('--no-browser', action='store_true', default=False, dest='no_browser',
                        help='Don\'t open the notebook in a browser after startup.'),
            Option('--use-pythonrc', action='store_true', dest='use_pythonrc',
                        help='Tells Flask to execute PYTHONSTARTUP file (BE CAREFULL WITH THIS!)'),
            Option('--print-sql', action='store_true', default=False,
                        help="Print SQL queries as they're executed"),
            Option('--dont-load', action='append', dest='dont_load', default=[],
                        help='Ignore autoloading of some apps/models. Can be used several times.'),
            Option('--quiet-load', action='store_true', default=False, dest='quiet_load',
                        help='Do not display loaded models messages'),
            Option('--vi', action='store_true', default=use_vi_mode(), dest='vi_mode',
                        help='Load Vi key bindings (for --ptpython and --ptipython)'),
        )

    def setup_pythonrc(self, **options):
        if options.get('use_pythonrc') is not True:
            return
        pythonrc = os.environ.get('PYTHONSTARTUP')
        if not all([pythonrc, os.path.isfile(pythonrc)]):
            return
        global_ns = {}
        with open(pythonrc) as rcfile:
            try:
                six.exec_(compile(rcfile.read(), pythonrc, 'exec'), global_ns)
            except NameError:
                print('Import pythonrc file {} failed'.format(pythonrc))
        self.context.update(global_ns)

    def setup_sql_printing(self, **options):
        print_sql = options.get('print_sql')
        if print_sql is not True:
            return

        db = self.context['db']
        db.engine.echo = True   # Used for SQLAlchemy

    def setup_imports(self, **options):
        app = self.context['app']
        quiet_load = options.get('quiet_load')
        dont_load = options.get('dont_load')
        model_aliases = app.config.get('SHELLPLUS_MODEL_ALIASES', {})
        basic_imports = {}
        pre_imports = app.config.get('SHELLPLUS_PRE_IMPORTS', {})
        post_imports = app.config.get('SHELLPLUS_POST_IMPORTS', {})

        import_directives = OrderedDict(pre_imports)
        import_directives.update(basic_imports)
        import_directives.update(post_imports)
        imported_objects = import_items(import_directives, quiet_load=quiet_load)
        self.context.update(imported_objects)

    def run(self, **options):
        """
        Runs the shell.  If no_bpython is False or use_bpython is True, then
        a BPython shell is run (if installed).  Else, if no_ipython is False or
        use_python is True then a IPython shell is run (if installed).

        :param options: defined in ``self.get_options``.
        """
        self.setup_sql_printing(**options)
        self.setup_pythonrc(**options)

        vi_mode = options['vi_mode']

        for key in ('notebook', 'plain', 'bpython', 'ptpython', 'ptipython', 'ipython'):
            if options.get(key):
                shell = key
                break
        else:
            shell = get_available_shell()

        self.setup_imports(**options)
        context = self.context

        if shell == 'notebook':
            no_browser = options['no_browser']
            notebook = get_notebook()
            notebook(no_browser=no_browser, display_name=self.banner)
        elif shell == 'bpython':
            from bpython import embed
            embed(banner=self.banner, locals_=context)
        elif shell == 'ptpython':
            from ptpython.repl import embed
            embed(banner=self.banner, user_ns=context, vi_mode=vi_mode)
        elif shell == 'ptipython':
            from ptpython.ipython import embed
            embed(user_ns=context, vi_mode=vi_mode)
        elif shell == 'ipython':
            from IPython import embed
            embed(user_ns=context)
        else:
            # Use basic python shell
            import code
            code.interact(self.banner, local=context)


def get_notebook():
    # import NotebookApp from IPython notebook
    try:
        from notebook.notebookapp import NotebookApp
    except ImportError:
        try:
            from IPython.html.notebookapp import NotebookApp
        except ImportError:
            from IPython.frontend.html.notebook import notebookapp
            NotebookApp = notebookapp.NotebookApp

    def run_notebook(no_browser=False, display_name='notebook'):
        app = NotebookApp.instance()

        ipython_arguments = []      # Will implement to set specific IPython configs
        notebook_arguments = []     # Will implement to set specific notebook configs

        if no_browser is True:
            notebook_arguments.append('--no-browser')

        if '--notebook-dir' not in notebook_arguments:
            notebook_arguments.extend(['--notebook-dir', '.'])

        install_kernel_spec(app, display_name, ipython_arguments)

        app.initialize(notebook_arguments)
        app.start()
    return run_notebook


def get_available_shell():
    """
    :return: The first available one in 'bpython', 'ptipython', 'ptpython', 'ipython'
    """
    shell = 'plain'
    from imp import find_module
    shell_deps = dict(
        bpython=('bpython',),
        ptipython=('ptpython', 'IPython'),
        ipython=('IPython',),
        ptpython=('ptpython',),
    )
    for _shell, deps in shell_deps.items():
        try:
            for mod in deps:
                if not find_module(mod):
                    continue
            shell = _shell
        except ImportError:
            continue
    return shell


def use_vi_mode():
    editor = os.environ.get('EDITOR')
    if not editor:
        return False
    editor = os.path.basename(editor)
    return editor.startswith('vi') or editor.endswith('vim')


def install_kernel_spec(app, display_name, ipython_arguments):
    """install an IPython >= 3.0 kernelspec that loads some extensions"""
    if app.kernel_spec_manager is None:
        try:
            from jupyter_client.kernelspec import KernelSpecManager
        except ImportError:
            from IPython.kernel.kernelspec import KernelSpecManager
        app.kernel_spec_manager = KernelSpecManager()
    ksm = app.kernel_spec_manager

    try_spec_names = [
        'python3' if six.PY3 else 'python2',
        'python',
    ]
    if isinstance(try_spec_names, six.string_types):
        try_spec_names = [try_spec_names]

    for spec_name in try_spec_names:
        try:
            ks = ksm.get_kernel_spec(spec_name)
            break
        except Exception as e:
            logging.warn(e)
            continue
    else:
        raise Exception("No notebook (Python) kernel specs found")

    ks.argv.extend(ipython_arguments)
    ks.display_name = display_name

    manage_py_dir, manage_py = os.path.split(os.path.realpath(sys.argv[0]))

    if manage_py == 'manage.py' and os.path.isdir(manage_py_dir) and manage_py_dir != os.getcwd():
        pythonpath = ks.env.get('PYTHONPATH', os.environ.get('PYTHONPATH', ''))
        pythonpath = pythonpath.split(':')
        if manage_py_dir not in pythonpath:
            pythonpath.append(manage_py_dir)

        ks.env['PYTHONPATH'] = ':'.join(filter(None, pythonpath))
