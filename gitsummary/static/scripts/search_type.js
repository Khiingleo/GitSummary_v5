$(document).ready(function () {
    $('#dynamic_post').submit(function (event) {
        event.preventDefault();

        var searchType = $("a.dropdown-item.active").data('search-type');

        if (!searchType) {
            this.action = '/error';
        } else if (searchType === 'users') {
            $('input[name="search_type"]').val('user');
            this.action = '/users';
        } else if (searchType === 'repositories') {
            $('input[name="search_type"]').val('repository');
            this.action = '/repos';
        }

        this.submit();
    });

    $('.dropdown-item').click(function (event) {
        event.preventDefault();
        $('.dropdown-item').removeClass('active');
        $(this).addClass('active');
        $('#dropdownMenuButton').text($(this).text());
    });
});