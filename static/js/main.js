/*global $, alert, console*/

// initialize
$(document).ready(function () {
  'use strict';
  $('#fullpage').fullpage({
    anchors: ['#front', '#new-student-info', '#materials'],
    css3: true,
    loopHorizontal: false,
    navigation: true,
    resize: false,
    verticalCentered: false
  });
  $('.circleWrap').lettering();
});
