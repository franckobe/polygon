$(function () {

    $('#search_form').on('submit',function (e) {
        e.preventDefault();
        $('#p').val(1);
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
            var pageinfo = resp.nbp > 0 ? "Page "+resp.curp+" sur "+resp.nbp+" - " : "";
            var resultat = resp.nb > 1 ? resp.nb+" résultats" : "Aucun resultat";
            var html = "<p>"+pageinfo+resultat+"  pour la recherche \""+word+"\"</p>";
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
    var prev = p === 1 ? 'disabled' : '';
    var next = p === nbp ? 'disabled' : '';
    var html = "";
    if ( nbp > 1 ) {
        html += "<ul class='pagination'>";

        html +=     "<li class='page-item " + prev + "'>";
        html +=         "<a href='#' class='page-link' data-p='" + ( p - 1 ) + "'>&laquo;</a>";
        html +=     "</li>";

        if ( p > 1 ) {
            html +=     "<li class='page-item'>";
            html +=         "<a href='#' class='page-link' data-p='1'>1</a>";
            html +=     "</li>";
        }
        if ( p > 2 ) {
            html +=     "<li class='page-item'>";
            html +=         "<a href='#' class='page-link' data-p='" + ( p - 1 ) + "'>" + ( p - 1 ) + "</a>";
            html +=     "</li>";
        }

        html +=     "<li class='page-item disabled'>";
        html +=         "<a href='#' class='page-link'>" + p + "</a>";
        html +=     "</li>";

        if ( p < nbp - 1 ) {
             html +=     "<li class='page-item'>";
             html +=         "<a href='#' class='page-link' data-p='" + ( p + 1 ) + "'>" + ( p + 1 ) + "</a>";
             html +=     "</li>";
        }
        if ( p < nbp ) {
            html +=     "<li class='page-item'>";
            html +=         "<a href='#' class='page-link' data-p='" + ( nbp ) + "'>" + ( nbp ) + "</a>";
            html +=     "</li>";
        }

        html +=     "<li class='page-item " + next + "'>";
        html +=         "<a href='#' class='page-link' data-p='" + ( p + 1 ) + "'>&raquo;</a>";
        html +=     "</li>";
        html += "</ul>";
    }
    return html
}