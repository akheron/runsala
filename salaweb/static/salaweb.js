// Django CSRF handling
$(function() {
    var csrftoken = (function(name) {
            var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    })('csrftoken'),
        csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


(function() {
    function tabs(tabs, stack) {
        if(!(tabs.length && stack.length)) {
            // Not on the main page
            return;
        }

        tabs.children(':first').addClass('active');
        stack.children(':first').addClass('active');

        tabs.find('li').click(function(e) {
            e.preventDefault();
            var repository = $(this).data('repository');

            tabs.children().removeClass('active');
            tabs.children('[data-repository=' + repository + ']')
                .addClass('active');

            stack.children().removeClass('active');
            stack.children('[data-repository=' + repository + ']')
                .addClass('active');
        });
    };

    function repository(el) {
        var prompt = $('#password-prompt'),
            form = prompt.find('form'),
            password = form.find('[name=password]');

        var open = function(e) {
            var path = $(this).attr('href');
            e.preventDefault();

            password.val('');
            form.off('submit').on('submit', function(e) {
                e.preventDefault();
                load(path, password.val());
            });
            prompt.modal();
        };

        var load = function(path, pw) {
            $.ajax({
                url: 'ajax/' + path,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({password: pw})
            }).done(function(data) {
                console.log(data);
            });
        };

        el.on('click', 'a', open);
    };

    $(function() {
        tabs($('.navbar .tabs'), $('.stack'));
        repository($('.stack > div'));
    });
})();
