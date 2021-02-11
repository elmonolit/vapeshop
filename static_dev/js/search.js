$(document).ready(function () {
    $('#searchbox').keyup(function () {
        var query;
        query = $(this).val();
        if (query !== ""){
        $.get('/search/', {searchbox:query}, function (data) {
            $('#searchres').html(data);
        });
        }
        else{
            $('#searchres').html('')
        }

    });
});