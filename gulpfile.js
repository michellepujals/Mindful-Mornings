"use strict";

const gulp = require('gulp');
const browserify = require('browserify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');
const sourcemaps = require('gulp-sourcemaps');

const config = {
  paths: {
    jsx: './src/**/*.jsx',
    mainJs: './src/index.jsx',
    dist: './static'
  }
}

gulp.task('jsx', () => {
  browserify(config.paths.mainJs)
    .transform('babelify', {
      presets: [
        '@babel/preset-env',
        '@babel/preset-react'
        // '@babel/plugin-proposal-class-properties'
      ],
      sourceMaps: true
    })
    .bundle()
    .on('error', console.error.bind(console))
    .pipe(source('bundle.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(config.paths.dist));
});

gulp.task('default', ['jsx']);
