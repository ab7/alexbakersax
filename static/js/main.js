/*global $, alert, console, matchMedia*/

// media query change
function widthChange(mq, overflow) {
  'use strict';
  var hash, studentSidebar;
  hash = window.location.hash;
  if (mq.matches) {
    // add css if js-enabled
    $('.saxBodyTop').show();
    $('.title').css({'margin': 0, 'max-width': '300px'});

    // initialize fullpagejs
    $('#fullpage').fullpage({
      afterRender: function () {
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
  var mq, media, overflow, bisKey, bisKeyMain, frontNav;

  // media query event handler
  overflow = false;
  if (window.location.href.indexOf('student') > -1) {
    media = '(min-width: 800px)';
    overflow = true;
  } else {
    media = '(min-width: 800px)';
  }
  if (matchMedia) {
    mq = window.matchMedia(media);
    mq.addListener(widthChange);
    widthChange(mq, overflow);
  }

  // initialize letteringjs
  $('.circleWrap').lettering();

  // button animation
  bisKey = $('.bisKey');
  bisKeyMain = $('.bisKeyMain');
  $('.bisKeyPearl').mousedown(function () {
    bisKey.animate({top: '+=.5em'}, 100, function () {
      bisKeyMain.css({'box-shadow': 'none'});
    });
  }).mouseup(function () {
    bisKey.animate({top: '-=.5em'}, 100, function () {
      bisKeyMain.css({'box-shadow': '-4px 5px 5px 0px rgba(72, 72, 72, 0.22)'});
    });
  });

  // nav bar control
  frontNav = $('.frontNav');
  $(window).on('hashchange', function () {
    frontNav.hide();
    if (window.location.hash !== '#full') {
      frontNav.fadeIn(2000);
    }
  });
});
