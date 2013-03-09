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
        el.find('a').click(function(e) {
            e.preventDefault();
            $('#password-prompt').modal();
        });
    };

    $(function() {
        tabs($('.navbar .tabs'), $('.stack'));
        repository($('.stack > div'));
    });
})();
