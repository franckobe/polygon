$(function () {

    $('#search_form').on('submit',function (e) {
        e.preventDefault();
        postSearch($(this));
    });
    $(document).on('click','.pagination li:not(.disabled) a',function (e) {
        e.preventDefault();
        $('#p').val( $(this).attr('data-p') );
        postSearch($('#search_form'));
    });

    $('.form_crawl').on('submit',function (e) {
        e.preventDefault();
        var token = getCookie('token');
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            headers: {
                'Authorization': "Token " + token
            },
            dataType: 'json',
            data: $(this).serialize(),
            success: function (data) {
                alert("Recherche lancée !")
            }
        })
    });

});

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function postSearch(form) {
    var token = getCookie('token');
    var word = $('#q').val();
    var p = $('#p');
    $.ajax({
        url: form.attr('action'),
        type: 'GET',
        headers: {
            'Authorization': "Token " + token
        },
        dataType: 'json',
        data: form.serialize(),
        success: function (resp) {
            var html = "<p>Page "+resp.curp+" sur "+resp.nbp+" - "+resp.nb+" résultats pour la recherche "+word+"</p>";
            resp.results.forEach(function (page) {
                html += "<div class='result'>";
                html +=     "<h3><a href='"+page.url+"'>"+page.title+"</a></h3>";
                html +=     "<h5>"+page.url+"</h5>";
                html += "</div>";
            });
            html += pagination(parseInt(p.val()), parseInt(resp.nbp));
            p.val(resp.curp);
            $('#results').html(html);
        }
    })
}

function pagination(p, nbp) {
    var first = p === 1 ? 'disabled' : '';
    var last = p === nbp ? 'disabled' : '';
    var html = "";
    html += "<ul class='pagination'>";

    html +=     "<li class='page-item " + first + "'>";
    html +=         "<a href='#' class='page-link' data-p='" + ( p - 1 ) + "'>&laquo;</a>";
    html +=     "</li>";

    if ( p > 1 ) {
        html +=     "<li class='page-item'>";
        html +=         "<a href='#' class='page-link' data-p='" + ( p - 1 ) + "'>" + ( p - 1 ) + "</a>";
        html +=     "</li>";
    }

    html +=     "<li class='page-item disabled'>";
    html +=         "<a href='#' class='page-link'>" + p + "</a>";
    html +=     "</li>";

    if ( p < nbp ) {
         html +=     "<li class='page-item'>";
         html +=         "<a href='#' class='page-link' data-p='" + ( p + 1 ) + "'>" + ( p + 1 ) + "</a>";
         html +=     "</li>";
    }

    html +=     "<li class='page-item " + last + "'>";
    html +=         "<a href='#' class='page-link' data-p='" + ( p + 1 ) + "'>&raquo;</a>";
    html +=     "</li>";
    html += "</ul>";
    return html
}