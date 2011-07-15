$(function() {
  var window = $(window);
  
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
  
  $('.bookmarklet form button[type="submit"]').click(function(ev) {
    ev.preventDefault();
    $('form').submit(function() {
      alert('got here');
      window.close();
    });
  });

  $('.bookmarklet input[name="description"]').val(unescape(document.location.href.split('u=')[1]));
});