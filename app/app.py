import bottle
from views import views

@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='assets')

#run python -m bottle --debug --reload main
#bottle.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
