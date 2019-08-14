// used to created the counts function on the addrecipe and edit recipe pages
(function($) {
  'use strict';

  $.fn.countChar = function() {

    return this.each(function(i, element) {
      $(element).keyup(function updateCharCounter() {

        var $me = $(this),
          maxLength = parseInt($me.attr('maxlength'), 10),
          charCount = $me.val().length,
          $counter = $me.siblings('.limit');

          $counter.text('limit: ' + maxLength + ' characters. remaining: ' + (maxLength - charCount));
      });
    });
  };
}(jQuery));
