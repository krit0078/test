jQuery(document).ready(function ($) {
  "use strict";

  //Contact
  $('form.php-email-form').submit(function () {

    var f = $(this).find('.form-group'),
      ferror = false,
      emailExp = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i;

    f.children('input').each(function () { // run all inputs

      var i = $(this); // current input
      var rule = i.attr('data-rule');

      if (rule !== undefined) {
        var ierror = false; // error flag for current input
        var pos = rule.indexOf(':', 0);
        if (pos >= 0) {
          var exp = rule.substr(pos + 1, rule.length);
          rule = rule.substr(0, pos);
        } else {
          rule = rule.substr(pos + 1, rule.length);
        }

        switch (rule) {
          case 'required':
            if (i.val() === '') {
              ferror = ierror = true;
            }
            break;

          case 'minlen':
            if (i.val().length < parseInt(exp)) {
              ferror = ierror = true;
            }
            break;

          case 'email':
            if (!emailExp.test(i.val())) {
              ferror = ierror = true;
            }
            break;

          case 'checked':
            if (!i.is(':checked')) {
              ferror = ierror = true;
            }
            break;

          case 'regexp':
            exp = new RegExp(exp);
            if (!exp.test(i.val())) {
              ferror = ierror = true;
            }
            break;
        }
        i.next('.validate').html((ierror ? (i.attr('data-msg') !== undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }
    });
    f.children('textarea').each(function () { // run all inputs

      var i = $(this); // current input
      var rule = i.attr('data-rule');

      if (rule !== undefined) {
        var ierror = false; // error flag for current input
        var pos = rule.indexOf(':', 0);
        if (pos >= 0) {
          var exp = rule.substr(pos + 1, rule.length);
          rule = rule.substr(0, pos);
        } else {
          rule = rule.substr(pos + 1, rule.length);
        }

        switch (rule) {
          case 'required':
            if (i.val() === '') {
              ferror = ierror = true;
            }
            break;

          case 'minlen':
            if (i.val().length < parseInt(exp)) {
              ferror = ierror = true;
            }
            break;
        }
        i.next('.validate').html((ierror ? (i.attr('data-msg') != undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }
    });
    if (ferror) return false;
    else var str = $(this).serialize();

    var this_form = $(this);
    var action = $(this).attr('action');
    var method = $(this).attr('method');

    if (!action) {
      this_form.find('.loading').slideUp();
      this_form.find('.error-message').slideDown().html('The form action property is not set!');
      return false;
    }

    this_form.find('.sent-message').slideUp();
    this_form.find('.error-message').slideUp();
    this_form.find('.loading').slideDown();

    const password = $('#id_password');
    const repassword = $('#id_re_password');

    if (password.val() != repassword.val()) {
      this_form.find('.loading').slideUp();
      repassword.addClass('is-invalid');
      return false;
    } else {
      repassword.removeClass('is-invalid');
      this_form.find('.loading').slideDown();
    }

    const edlevel = $('#id_edlevel');
    if (edlevel.val() == 0) {
      this_form.find('.loading').slideUp();
      edlevel.addClass('is-invalid');
      return false;
    } else {
      edlevel.removeClass('is-invalid');
    }

    const ed_sublevel = $('#id_ed_sublevel');
    if (ed_sublevel.val() == 0) {
      this_form.find('.loading').slideUp();
      ed_sublevel.addClass('is-invalid');
      return false;
    } else {
      ed_sublevel.removeClass('is-invalid');
    }

    const user_type = $('#id_user_type');
    if (user_type.val() == 0) {
      this_form.find('.loading').slideUp();
      user_type.addClass('is-invalid');
      return false;
    } else {
      user_type.removeClass('is-invalid');
    }

    const email = $('#email');
    if (email.hasClass('is-invalid')) {
      this_form.find('.loading').slideUp();
      return false;
    }

    $.ajax({
      type: method,
      url: action,
      data: str,
      success: function (data) {
        if (data.status == 1) {
          this_form.find('.loading').slideUp();
          this_form.find('.sent-message').slideDown();
          this_form.find("input:not(input[type=submit]), textarea").val('');
          setTimeout(window.location.replace("/login/"), 3000);
          
        } else {
          this_form.find('.loading').slideUp();
          this_form.find('.error-message').slideDown().html(msg);
        }
      }
    });
    return false;
  });

});
