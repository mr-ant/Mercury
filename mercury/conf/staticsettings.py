from . import basic


class StaticSettings(object):
    def __getattr__(self, item):
        try:
            return getattr(basic, item)
        except AttributeError:
            pass

        raise AttributeError("%s setting is not defined!" % item)
