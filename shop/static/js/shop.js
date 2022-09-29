$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html("");
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };

  var ContactUsloadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#contact-modal .modal-content").html("");
        $("#contact-modal").modal("show");
      },
      success: function (data) {
          $("#contact-modal .modal-content").html(data.html_form);
        }
    });
  };

  var ContactUssaveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          alert("Your message was successfully send to administration, wait for our response on your email.");
          $("#contact-modal").modal("hide");
        }
        else {
          $("#contact-modal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-book").modal("hide");
          window.location='/'
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var loginForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-book").modal("hide");
          window.location='/'
        }
        else {
          alert("Wrong password or username.");
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var change_passwordForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-book").modal("hide");
          alert("Password successfully changed!");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */
  $(".js-shop").click(loadForm);
  $(".contact-us").click(ContactUsloadForm);

  // Create user
  $("#modal-book").on("submit", ".js-create-user", saveForm);

  // Login user
  $("#modal-book").on("submit", ".js-login-form", loginForm);

  // Change password
  $("#modal-book").on("submit", ".js-change_password-form", change_passwordForm);

  // Contact us
  $("#contact-modal").on("submit", ".js-contact-us", ContactUssaveForm);

});
