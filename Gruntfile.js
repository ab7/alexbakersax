/*global module*/

module.exports = function (grunt) {
  'use strict';
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    autoprefixer: {
      single_file: {
        options: {
          // Target-specific options go here.
        },
        src: 'static/styles/main.css',
        dest: 'static/styles/main.prefixed.css'
      }
    }
  });
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.registerTask('default', ['autoprefixer']);
};
