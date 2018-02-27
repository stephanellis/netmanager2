from pyramid.config import Configurator
from netmanager2.couchtools import CouchConfigurator
from netmanager2.libnm2 import NetManager


def get_nm(request):
    return request.registry.nm


def get_couch(request):
    return request.registry.cc.get_db()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.registry.cc = CouchConfigurator(
            settings["couchdb.server"],
            settings["couchdb.db"],
            designdocs=settings["couchdb.designdocs"]
    )
    config.registry.nm = NetManager(config.registry.cc)
    config.add_request_method(get_nm, "nm", reify=True)
    config.add_request_method(get_couch, "db", reify=True)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
