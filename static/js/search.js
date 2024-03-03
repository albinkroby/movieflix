$(document).ready(function () {
    $('#search-bar').on('input', function () {
        var query = $(this).val();

        $.ajax({
            type: 'GET',
            url: '{% url "search_movies" %}',  // Update this with the actual URL for your search view
            data: {
                'q': query
            },
            success: function (data) {
                $('#search-results-dropdown').empty();
                data.forEach(function (result) {
                    var resultItem = $('<li><a class="dropdown-item" href="' + result.url + '">' + result.title + '</a></li>');
                    $('#search-results-dropdown').append(resultItem);
                });
            }
        });
    });
});
