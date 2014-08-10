/*global $, alert*/

// initialize
$(document).ready(function () {
  'use strict';
  $('#fullpage').fullpage({
    css3: true,
    loopHorizontal: false,
    resize: false,
    verticalCentered: false
  });
  $('.circleWrap').lettering();
});
