/**
 * Created by PyCharm.
 * User: mike
 * Date: 18.10.11
 * Time: 21:23
 * To change this template use File | Settings | File Templates.
 */

function feedtest() {
    url = $('#feedurl').val();
    if (!url) {
        $('#testfeedresult').show();
        $('#testfeedresult').html('No url!');
    } else {
        $.ajax({
            type: "GET",
            url: "/my/feedtest/",
            data: "url=" + url
        }).done(function(msg) {
                $('#testfeedresult').show();
                $('#testfeedresult').html(msg);
            });

    }

}

function vkontakteauth(backurl) {
    var url = "http://api.vkontakte.ru/oauth/authorize?client_id=2663418&scope=wall,groups,offline&response_type=token";
        //"&redirect_uri=" + backurl
    auth = window.open(url, "test");
    //document.location.href = url;
}

function foursquareauth(backurl) {
    var url = "https://foursquare.com/oauth2/authenticate?client_id=TIINZSMUJFLCRWFU2RL1GPLBJRQI1HQUFETKWOLNPQVBC21L&response_type=code&redirect_uri=" + backurl
    document.location.href = url;
}

function twitterauth(backurl, redirecturl) {
    document.location.href = redirecturl;
}

function facebookauth(redirecturl) {
    document.location.href = redirecturl;
}