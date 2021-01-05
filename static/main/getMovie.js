var index = 0

$(function () {
    $.ajax({
        url: "/data/Uid",
        type: "GET",
        dataType: "text",
        success: function (data) {
            $("#uid").html(data)
            $("#uid1").html(data)
        }
    })

    $.ajax({
        url: "/data/getMovieName",
        type: "GET",
        dataType: "json",
        success: function (data) {
            for (i=0;i<data.movieName.length;i++){
                $("#movieList").html(
                    $("#movieList").html() +
                    "<tr><th>" + data.movieName[i] + "</th><th>" + data.rating[i].toFixed(2) + "</th></tr>"
                );
            }
        },
        error: function () {
            alert("传递失败");
        }
    })

})
