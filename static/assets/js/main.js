/**
* Template Name: Bocor - v2.0.0
* Template URL: https://bootstrapmade.com/bocor-bootstrap-template-nice-animation/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
!(function ($) {
  "use strict";

  // Smooth scroll for the navigation menu and links with .scrollto classes
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function (e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      e.preventDefault();
      var target = $(this.hash);
      if (target.length) {

        var scrollto = target.offset().top;

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function (e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function (e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });

    $(document).click(function (e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });

  $('.back-to-top').click(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

  // Porfolio isotope and filter
  $(window).on('load', function () {
    var portfolioIsotope = $('.portfolio-container').isotope({
      itemSelector: '.portfolio-item',
      layoutMode: 'fitRows'
    });

    $('#portfolio-flters li').on('click', function () {
      $("#portfolio-flters li").removeClass('filter-active');
      $(this).addClass('filter-active');

      portfolioIsotope.isotope({
        filter: $(this).data('filter')
      });
    });

    // Initiate venobox (lightbox feature used in portofilo)
    $(document).ready(function () {
      $('.venobox').venobox();
    });
  });

  // Initi AOS
  AOS.init({
    duration: 800,
    easing: "ease-in-out"
  });

  $(document).ready(function () {
    $('#insert_link').keypress(function (e) {
      if (e.which == 13) {
        $('.dropdown-menu').dropdown('hide');
        let txt = "<a class='btn-link' href='" + $(this).val() + "' target='_blank'>" + $(this).val() + "</button>";
        $('#steam_div').append(txt);
        $(this).val("");
        return false;
      }
    });

  });

})(jQuery);

function check_http(e) {
  let paste = (event.clipboardData || window.clipboardData).getData('text');

  let expression = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi;
  let regex = new RegExp(expression);

  const selection = window.getSelection();
  let url=""
  if (paste.match(regex)) {
    url = paste;
    let pattern = /^((http|https|ftp):\/\/)/;

    if (!pattern.test(url)) {
      url = "http://" + paste;
    }

    if (!selection.rangeCount) return false;
    selection.deleteFromDocument;
    let a = document.createElement("a");
    a.href = url;
    a.text = paste;
    a.target = "_blank";
    selection.getRangeAt(0).insertNode(a);
  }
  else {
    selection.getRangeAt(0).insertNode(document.createTextNode(paste));
  }
  selection.collapseToEnd();
  event.preventDefault();

  return url;
}

function load_og(url,target){
  let show_file = $('#show_file');
  $.ajax('/ajax/fetch_og', {
          method: 'GET',
          data: { 'url': url, 'target': target },
          dataType: 'json',
          success: function (data) {
              let d = data.og;
              let txt = "<a href='" + d.url + "' style='text-decoration: none;color: #000;' target='_blank'><div class='row no-gutters rounded opengraph mb-2'>";
              txt += "<div class='col-3'><img src='" + d.image + "' style='width: 100%;'></div>";
              txt += "<div class='col-9 p-3 bg-light'><h5>" + d.title + "</h5><p>" + d.description + "</p></div></div>";
              txt += "<input type='hidden' name='link_id[]' value='" + d.id + "'></a>";
              console.log(data);
              show_file.append(txt);
          },
          error: function () {
              // alert("ไม่สามารถโหลดข้อมูลได้");
          }
      });

}