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
        var submit = function(e, link, form) {
            e.preventDefault();
            load(
                $(link).attr('href'),
                $(form).find('[name=password]').val()
            );
        };

        var load = function(path, password) {
            console.log(path, password);
        };

        el.find('a').click(function(e) {
            var link = this;

            e.preventDefault();
            $('#password-prompt')
                .find('form').off('submit').on('submit', function(e) {
                    submit(e, link, this);
                }).end()
                .modal();
        });
    };

    $(function() {
        tabs($('.navbar .tabs'), $('.stack'));
        repository($('.stack > div'));
    });
})();
