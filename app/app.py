import bottle, os, sys, config

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

from config import l
from views import views
from models.models import Base

#Almost every page uses utf-8.
#Now we don't have to worry about it
reload(sys)
sys.setdefaultencoding('utf-8')

#Database init
engine = create_engine(config.DATABASE_URL, echo=True)
if config.INIT_DB: Base.metadata.create_all(engine)
plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata, # required only if create=True
    keyword='db',  # injected into session routes
    commit=True    # commit changes after route is executed
)
bottle.install(plugin)

@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='assets')

#run python -m bottle --debug --reload main
if __name__ == "__main__":
    if config.DEV and 'BOTTLE_CHILD' not in os.environ:
        l.info('Using reloader, spawning first child.')
    else:
        l.info("Starting %s Server", ("Development" if config.DEV else "Production"))
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
    bottle.run(host=config.HOST, port=config.PORT, debug=config.DEV, reloader=config.DEV)
