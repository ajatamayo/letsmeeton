$(document).ready(function() {

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    $('body').on('click', '.not-attending', function() {
        var $this = $(this);

        $.ajax({
            url: '',
            method: 'POST',
            data: $this.data(),
            success: function(data) {
                var $signup = $('<div class="signup you">YOU</div>');
                $signup.css('width', data.width + '%');
                $signup.data('signup', data.signup);
                $signup.attr('title', 'Click to remove your confirmation.');
                $this.removeClass('not-attending');
                $this.removeAttr('title');
                $this.find('.signups').append($signup);
            }
        });
    });

    $('body').on('click', '.signup.you', function() {
        var $this = $(this);

        $.ajax({
            url: '',
            method: 'POST',
            data: $this.data(),
            success: function(data) {
                var $timeofday = $this.closest('.timeofday-wrapper');
                $timeofday.addClass('not-attending');
                $timeofday.attr('title', 'Click to confirm your availability!');
                $this.remove();
            }
        });
    });
});