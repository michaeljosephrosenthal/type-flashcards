var path = require('path'),
    gulp = require('gulp'),
    cache = require('gulp-cached'),
    less = require('gulp-less'),
    livereload = require('gulp-livereload'),
    runSequence = require('run-sequence'),
    plumber = require('gulp-plumber'),
    sourcemaps = require('gulp-sourcemaps'),
    reactify = require('reactify'),
    browserify = require('browserify'),
    watchify = require('watchify'),
    textToGulp = require('vinyl-source-stream');

var jsx_srcs = '../app/jsx/*jsx';
var app_root = '../app/jsx/app.js';
var app_dest = 'app.js';
var js_dir = '../app/assets/js/';

var less_srcs = '../app/less/**/*less';
var css_dir = '../app/assets/css/';

gulp.task('compileLess', function() {
   console.log('Updating Less!');
   gulp.src(less_srcs)
      .pipe(sourcemaps.init())
      .pipe(less())
      .pipe(plumber())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(css_dir))
      .pipe(livereload());
});

gulp.task('watchLess', function(){
     gulp.watch(less_srcs, ['compileLess']);
});

gulp.task('compileJS', function() {
    var bundler = browserify({
        entries: [app_root],
        transform: [reactify],
        debug: true, // only way to get sourcemaps
        cache: {},
        packageCache: {},
        fullPaths: true // Requirement of watchify
    });
    var watcher = watchify(bundler);

    return watcher
        .on('update', function() { // When any files update
            var updateStart = Date.now();
            console.log('Updating JS!');
            watcher.bundle() // Create new bundle that uses the cache for high performance
                .pipe(textToGulp(app_dest))
                // This is where you add uglifying etc.
                .pipe(gulp.dest(js_dir));
            console.log('Updated!', (Date.now() - updateStart) + 'ms');
        })
        .bundle() // Create the initial bundle when starting the task
        .pipe(plumber())
        .pipe(textToGulp(app_dest))
        .pipe(gulp.dest(js_dir))
        .pipe(livereload());
});

// The default task (called when you run `gulp`)
gulp.task('default', ['compileLess', 'watchLess', 'compileJS']);
