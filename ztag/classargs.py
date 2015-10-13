import argparse
import importlib


def subclass_of(cls):

    def check_class(class_path):
        path_parts = class_path.split('.')
        if len(path_parts) < 2:
            msg = "requires a fully-qualified class name"
            raise argparse.ArgumentTypeError(msg)
        class_name = path_parts[-1]
        module_name = '.'.join(path_parts[0:-1])
        try:
            m = importlib.import_module(module_name)
        except ImportError:
            msg = "unable to import %s" % module_name
            raise argparse.ArgumentTypeError(msg)
        kls = getattr(m, class_name, None)
        if kls is None:
            msg = "class %s not a member of module %s" % (class_name,
                                                          module_name)
            raise argparse.ArgumentTypeError(msg)
        if not issubclass(kls, cls):
            msg = "class %s is not a subclass of %s" % (class_name,
                                                        cls.__name__)
            raise argparse.ArgumentTypeError(msg)
        return kls

    return check_class
