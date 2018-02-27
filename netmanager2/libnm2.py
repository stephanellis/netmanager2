#
# libnm2 - the meat and potatoes of the netmanager software
#

class NetManager(object):
    """
    the main app class
    """
    def __init__(self, cc):
        self.cc = cc

    @property
    def db(self):
        return self.cc.get_db()


class Operator(object):
    pass


class Net(object):
    pass


class CheckIn(object):
    pass
