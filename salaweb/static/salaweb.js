(function() {
    var tabs = function(tabs, stack) {
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

    var repository = function(el) {
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
