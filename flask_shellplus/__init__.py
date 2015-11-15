#!/usr/bin/env python
# coding: utf-8
from flask import current_app
from flask.ext.script import Command, Option


__version__ = '0.0.1'


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
        # TODOs:
        #    Option('--notebook', action='store_true', dest='notebook',
        #                help='Tells Flask to use IPython Notebook.'),
        #    Option('--kernel', action='store_true', dest='kernel',
        #                help='Tells Flask to start an IPython Kernel.'),
        #    Option('--use-pythonrc', action='store_true', dest='use_pythonrc',
        #                help='Tells Flask to execute PYTHONSTARTUP file (BE CAREFULL WITH THIS!)'),
        #    Option('--print-sql', action='store_true', default=False,
        #                help="Print SQL queries as they're executed"),
        #    Option('--dont-load', action='append', dest='dont_load', default=[],
        #                help='Ignore autoloading of some apps/models. Can be used several times.'),
        #    Option('--quiet-load', action='store_true', default=False, dest='quiet_load',
        #                help='Do not display loaded models messages'),
        #    Option('--vi', action='store_true', default=use_vi_mode(), dest='vi_mode',
        #                help='Load Vi key bindings (for --ptpython and --ptipython)'),
        #    Option('--no-browser', action='store_true', default=False, dest='no_browser',
        #                help='Don\'t open the notebook in a browser after startup.'),
        )

    def run(self, **options):
        """
        Runs the shell.  If no_bpython is False or use_bpython is True, then
        a BPython shell is run (if installed).  Else, if no_ipython is False or
        use_python is True then a IPython shell is run (if installed).

        :param options: defined in ``self.get_options``.
        """
        for key in ('plain', 'bpython', 'ptpython', 'ptipython', 'ipython'):
            if options.get(key):
                shell = key
                break
        else:
            shell = get_available_shell()

        context = self.context

        if shell == 'bpython':
            from bpython import embed
            embed(banner=self.banner, locals_=context)
        elif shell == 'ptpython':
            from ptpython.repl import embed
            embed(banner=self.banner, user_ns=context)
        elif shell == 'ptipython':
            from ptpython.ipython import embed
            embed(user_ns=context)
        elif shell == 'ipython':
            from IPython import embed
            embed(user_ns=context)
        else:
            # Use basic python shell
            import code
            code.interact(self.banner, local=context)


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
