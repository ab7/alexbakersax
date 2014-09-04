/*global $, alert, console, matchMedia*/

// media query change
function widthChange(mq) {
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
      autoScrolling: false,
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
  var mq, media, bisKey, bisKeyMain, frontNav;

  // media query event handler
  media = '(min-width: 800px)';

  if (matchMedia) {
    mq = window.matchMedia(media);
    mq.addListener(widthChange);
    widthChange(mq);
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
  if (window.location.hash !== '#full' && window.location.hash !== '') {
    frontNav.finish().fadeIn(4000);
  }
  $(window).on('hashchange', function () {
    frontNav.hide();
    if (window.location.hash !== '#full') {
      frontNav.finish().fadeIn(2000);
    }
  });
});

