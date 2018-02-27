# quick and dirty concept for managing design docs

from pyramid.path import AssetResolver
import pycouchdb
from pycouchdb.exceptions import NotFound
from logzero import logger as log
import json
import os


class CouchConfigurator:
    """
    configurator for a couchdb installation
    """
    def __init__(self, server, db, designdocs=None):
        log.debug("setting up couchdb {} on server {}".format(server, db))
        self.server = server
        self.db = db
        self.couch_server = pycouchdb.Server(self.server)
        self.couchdb = None
        try:
            self.couchdb = self.couch_server.database(db)
            log.debug("db exists")
        except NotFound:
            log.debug("db not found, creating it")
            self.couch_server.create(db)
            self.couchdb = self.couch_server.database(db)
        self.designdocs = designdocs # this is a pyramid asset spec
        if self.designdocs:
            log.debug("updating design docs")
            self.update_designdocs()


    def get_db(self):
        return self.couchdb


    def get_designdocs(self):
        r = AssetResolver(self.designdocs.split(":")[0])
        p = r.resolve(self.designdocs).abspath()
        designdocs = dict()
        for d, dirs, files in os.walk(p):
            log.debug("{}, {}, {}".format(d, dirs, files))
            if "map.js" in files: # we have what should be a view directory
                vn = d.split(p + "/")[1].split("/")
                log.debug("view name is {} parsed from {}".format(vn, d))
                dd = vn[0]
                view = vn[1]
                if dd not in designdocs:
                    designdocs[dd] = dict()
                    designdocs[dd]['views'] = dict()
                if view not in designdocs[dd]['views']:
                    designdocs[dd]['views'][view] = dict()
                designdocs[dd]['views'][view]['map'] = self.loadfile(d + "/map.js")
                if "reduce.js" in files:
                    designdocs[dd]['views'][view]['reduce'] = self.loadfile(d + "/reduce.js")
        return designdocs


    def update_designdocs(self):
        dds = self.get_designdocs()
        log.debug(json.dumps(dds, indent=2))
        for dd in dds:
            log.debug("updating designdoc {}".format(dd))
            id = "_design/{}".format(dd)
            cdd = None
            try:
                # if the design doc exists, check if there was a change
                cdd = self.couchdb.get(id)
                if cdd['views'] != dds[dd]['views']:
                    cdd['views'] = dds[dd]['views'] # update the view
                    self.couchdb.save(cdd)
            except NotFound: # if the view doesn't exist, we create it here
                cdd = dict(
                    _id = id,
                    views = dds[dd]['views'],
                    language = "javascript"
                )
                self.couchdb.save(cdd)

        return True


    def loadfile(self, fp): # just reads all lines from the file
        with open(fp, "r") as f:
            return "".join(f.readlines())
