#
# libnm2 - the meat and potatoes of the netmanager software
#

from uuid import uuid4
from box import Box
from logzero import logger as log
from netmanager2.couchtools import Doc, Field

def generate_id():
    return str(uuid4())


class NetManager(object):
    """
    the main app class
    """
    def __init__(self, cc):
        self.cc = cc

    @property
    def db(self):
        return self.cc.get_db()


class Net(Doc):
    doctype = "net"
    desc = Field()
