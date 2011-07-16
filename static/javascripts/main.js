$(function() {
  $('.button.new').toggle(
    function(ev) {
      ev.preventDefault();
      $('.new_post').slideDown();
    },
    function(ev) {
      ev.preventDefault();
      $('.new_post').slideUp();
    }
  );
  
  $('.bookmarklet form').submit(function() {
    var self = $(this);
    $.post($('form').attr('action'), $('form').serializeArray(), function() {
      window.close();
    });
    return false;
  });

  $('.bookmarklet input[name="description"]').val(unescape(document.location.href.split('u=')[1]));
  
  
  $('.bookmarklet_button').hover(
    function() {
      $('.tooltip').fadeIn('fast');
    },
    function() {
      $('.tooltip').fadeOut('fast');
    }
  );

});