/*global $, alert, console, matchMedia*/

// media query change
function widthChange(mq, overflow) {
  'use strict';
  var hash;
  hash = window.location.hash;
  if (mq.matches) {
    // add css if js-enabled
    $('.saxBodyTop').show();
    $('.title').css({'margin': 0, 'max-width': '300px'});

    // initialize fullpagejs
    $('#fullpage').fullpage({
      afterRender: function () {
        var studentSidebar;
        studentSidebar = $('.studentPortal');
        if (studentSidebar.length) {
          studentSidebar.show();
        }
      },
      anchors: ['full', 'new-student-info', 'materials', 'contact'],
      css3: true,
      loopHorizontal: false,
      resize: false,
      scrollOverflow: overflow,
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
  var mq, media, overflow;
  overflow = false;
  if (window.location.href.indexOf('student') > -1) {
    media = '(min-width: 900px)';
    overflow = true;
  } else {
    media = '(min-width: 650px)';
  }
  if (matchMedia) {
    mq = window.matchMedia(media);
    mq.addListener(widthChange);
    widthChange(mq, overflow);
  }

  // initialize letteringjs
  $('.circleWrap').lettering();

  // button animation
  $('.bisKeyPearl').click(function () {
    var key;
    key = $('.bisKey');
    $('.bisKeyMain').css({'box-shadow': 'none'});
    key.animate({top: '+=.5em'}, 100, function () {
      key.animate({top: '-=.5em'}, 100);
      $('.bisKeyMain').css({'box-shadow': '-4px 5px 5px 0px rgba(72, 72, 72, 0.22)'});
    });
  });
});
