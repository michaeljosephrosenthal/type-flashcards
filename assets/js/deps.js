/* global cfg, def, fallback, req */
def(function() {
    cfg({
        'libs': {
            // prefix css$ for css cdns
            'css$bootstrap': {
                // if exports are loaded then asset is unneeded
                'exports': '.col-xs-12',
                // CDN url(s)
                'urls': [
                    '//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min',
                    '../assets/vendor/bootstrap-3.3.1.min'
                ]
            },
            'jQuery': {
                'urls': [
                    '//code.jquery.com/jquery-1.11.2.min.js',
                     '../assets/vendor/jquery-2.1.3.min.js'
                ]
            },
            'Bootstrap': {
                'exports': 'jQuery().modal',   // Bootstrap is hard to detect, so we use $().modal
                'deps': 'jQuery',
                'urls': [
                    '//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js',
                         '../assets/vendor/bootstrap-3.3.1.min.js'
                             ]
            },


            'css$styles': {
                'deps': 'css$bootstrap',
                'urls': '../assets/css/styles'
            },
            'script': {
                'deps': 'jQuery',
                'urls': '../assets/js/script.js'
            }
        }
    });
    req(function(css$bootstrap, css$styles, jQuery, Bootstrap, script) {
        console.log(fallback.stats());
    });
});
