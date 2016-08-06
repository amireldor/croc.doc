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
    Object.assign({}, watchify.args, {entries:  ['./src/js/main.js']})
));

function bundle() {
    return bundler.bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify error'))
        .pipe(source('static/crocfarm.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./dev-build'));
}
gulp.task('js', bundle);
bundler.on('update', bundle);
bundler.on('log', gutil.log);

// stuff
// ...

const indexHtmlPath = './src/index.html';

// more tasks
gulp.task('copy-html-dev', function () {
    gulp.src(indexHtmlPath).pipe(gulp.dest('./dev-build'));

});

gulp.task('copy-html-build', function () {
    gulp.src(indexHtmlPath).pipe(gulp.dest('./build'));
});

gulp.task('scss', function () {
});

gulp.task('dev', ['copy-html-dev', 'scss', 'js']);

gulp.task('default', function () {
    console.log('Hi.');
});
