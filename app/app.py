import bottle, os
from views import views

@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='assets')

#run python -m bottle --debug --reload main
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    DEV = os.environ.get("app_env", False) == "Dev"
    print "Starting " + ("Development" if DEV else "Production") + " Server"
    bottle.run(host='0.0.0.0', port=os.environ.get("PORT", 5000), debug=DEV, reloader=DEV)
