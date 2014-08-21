/*global $, alert, console, matchMedia*/

// media query change
function widthChange(mq) {
  'use strict';
  var hash;
  hash = window.location.hash;
  if (mq.matches) {
    $('.saxBodyTop').show();
    $('.title').css({'margin': 0, 'max-width': '300px'});
    $('#fullpage').fullpage({
      anchors: ['full', 'new-student-info', 'materials', 'contact'],
      css3: true,
      loopHorizontal: false,
      resize: false,
      verticalCentered: false
    });
  } else {
    if (hash !== '#mobile') {
      window.location.hash = '#mobile';
      location.reload();
    }
  }
}

// initialize
$(document).ready(function () {
  'use strict';

  // media query event handler
  if (matchMedia) {
    var mq = window.matchMedia("(min-width: 500px)");
    mq.addListener(widthChange);
    widthChange(mq);
  }

  $('.circleWrap').lettering();
});
