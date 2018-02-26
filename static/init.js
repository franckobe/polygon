$(function () {

    $('#search_form').on('submit',function (e) {
        e.preventDefault();
        var token = getCookie('token');
        var word = $('#q').val();
        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            headers: {
                'Authorization': "Token " + token
            },
            dataType: 'json',
            data: $(this).serialize(),
            success: function (resp) {
                var html = "<p>"+resp.length+" résultats pour la recherche "+word+"</p>";
                resp.forEach(function (res) {
                    html += "<div class='result'>";
                    html +=     "<h3><a href='"+res.url+"'>"+res.title+"</a></h3>";
                    html +=     "<h5>"+res.url+"</h5>";
                    html += "</div>";
                });
                $('#results').html(html);
            }
        })
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