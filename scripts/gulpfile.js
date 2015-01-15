var path = require('path');
var gulp = require('gulp');
var cache = require('gulp-cached');
var less = require('gulp-less');
var livereload = require('gulp-livereload');
var runSequence = require('run-sequence');
var plumber = require('gulp-plumber');
var sourcemaps = require('gulp-sourcemaps');

var less_srcs = '../app/less/*less'; 
var css_dir = '../app/assets/css/';

gulp.task('compileLess', function() {
    gulp.src(less_srcs)
        .pipe(sourcemaps.init())
        .pipe(plumber())
        .pipe(cache('less'))
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(css_dir));
});

// The default task (called when you run `gulp`)
gulp.task('default', function() {    
    livereload.listen(35730);  // port - 35730
    gulp.run('compileLess');        

    // Watch files and run tasks if they change
    gulp.watch(less_srcs).on('change', function(file) {
        var changed = css_dir + path.basename(file.path).replace('less', 'css');        
        console.log(changed);
        runSequence('compileLess', function(){            
            setTimeout(function(){
                livereload.changed(changed, 35730);
            }, 200);
        });
    });
});

