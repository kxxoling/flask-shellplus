# coding: utf-8
from __future__ import print_function
import six


def import_items(import_directives, style=None, quiet_load=False):
    """Import items in import_directives and return a list of imported items
    :param import_directives: target to be imported, should be a list of tuple in form of ``(module, target)``
    :param style: echo styling object, NotImplemented
    :param quiet_load: echo or not
    :return: a mapping of names and imported items
    """
    imported_objects = {}
    for module_name, target in import_directives.items():
        if target == '*':
            imported_objects.update(_import_all(module_name, quiet_load=quiet_load))
        elif isinstance(target, six.string_types):
            imported_objects.update(_import_item(module_name, target, quiet_load=quiet_load))
        else:
            imported_objects.update(_import_multi(module_name, target, quiet_load=quiet_load))
    return imported_objects


def _import_item(module_name, name, quiet_load=False):
    directive = '.'.join((module_name, name))
    try:
        imported_object = __import__(directive, {}, {}, name)
    except ImportError:
        if quiet_load is False:
            print("Unable to import %r" % directive)
        return {}
    else:
        if quiet_load is False:
            print("from %s import %s" % (module_name, name))
        return {name: imported_object}


def _import_multi(module_name, names, quiet_load=False):
    imported_objects = {}
    for name in names:
        imported_objects.update(_import_item(module_name, name, quiet_load=quiet_load))
    return imported_objects


def _import_all(module_name, quiet_load=False):
    imported_objects = {}
    module_obj = __import__(module_name, {}, {}, '*')
    for name in dir(module_obj):
        imported_objects[name] = getattr(module_obj, name)
    if quiet_load is False:
        print("from %s import *" % module_name)
    return imported_objects
