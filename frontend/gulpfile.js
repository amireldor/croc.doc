const gulp = require('gulp');
const gutil = require('gulp-util');

const browserify = require('browserify');
const watchify = require('watchify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');
const uglify = require('gulp-uglify');
const sourcemaps = require('gulp-sourcemaps');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const del = require('del');

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
        .pipe(gulp.dest('./build'));
}
gulp.task('js', bundle);
bundler.on('update', bundle);
bundler.on('log', gutil.log);

// stuff
// ...

const indexHtmlPath = './src/index.html';
const scssPath = './src/scss/**/*.scss';

// more tasks

// Delete build folder
gulp.task('clean', function () {
    return del('./build/**/*');    
});

gulp.task('copy-html', function () {
    gulp.src(indexHtmlPath).pipe(gulp.dest('./build'));
});

gulp.task('html-watch', function () {
    return gulp
    .watch(indexHtmlPath, ['copy-html'])
    .on('change', function (event) {
        console.log('I think HTML changed: ', event.path, event.type);
    });
});

gulp.task('sass', function () {
    const sassOptions = {
        errLogToConsole: true,
        outputStyle: 'expanded'
    };
    return gulp
        .src(scssPath)
        .pipe(sourcemaps.init())
        .pipe(sass(sassOptions).on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(autoprefixer())
        .pipe(gulp.dest('./build/static'));

});

gulp.task('sass-watch', function () {
    return gulp
        .watch(scssPath, ['sass'])
        .on('change', function (event) {
            console.log(event.path + ' was ' + event.type);
        });
});

gulp.task('dev', ['clean', 'copy-html', 'html-watch', 'sass', 'sass-watch', 'js']);

gulp.task('default', function () {
    console.log('Hi.');
});
