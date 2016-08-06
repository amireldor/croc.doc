const gulp = require('gulp');
const gutil = require('gulp-util');

const browserify = require('browserify');
const watchify = require('watchify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');
const uglify = require('gulp-uglify');
const sourcemaps = require('gulp-sourcemaps');

// Do watchify/browiserfy magic
const bundler = watchify(browserify(
    Object.assign({}, watchify.args, {entries:  ['./src/main.js']})
));

function bundle() {
    return bundler.bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify error'))
        .pipe(source('crocfarm.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./build'));
}
gulp.task('js', bundle);
bundler.on('update', bundle);
bundler.on('log', gutil.log);

gulp.task('default', function () {
    console.log('Hi.');
});
