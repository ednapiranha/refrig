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
  
  $('.new_post form, .edit_post form').submit(function(ev) {
     ev.preventDefault();
     var self = $(this);
     self.find('button').attr('disabled', 'disabled'); 
     $.post($('form').attr('action'), $('form').serializeArray(), function() {
        self.find('button').removeAttr('disabled');
        document.location.href = '/yours';
     });
     return false;
  });
  
  $('.bookmarklet form').submit(function(ev) {
    ev.preventDefault();
    var self = $(this);
    self.find('button').attr('disabled', 'disabled'); 
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

  $('input.search').keyup(function() {
    var current_text = $(this).val().toLowerCase();
    if(current_text.length > 0) {
      $('.tag_list > li').each(function(idx, el) {
        var self = $(el);
        if(self.find('a').text().indexOf(current_text.toLowerCase()) < 0) {
          self.hide();
        } else {
          self.show();
        }
      });
    } else {
      $('.tag_list > li').show();
    }
  });
});