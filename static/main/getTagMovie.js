var index = 0

$(function () {

    $.ajax({
        url: "/data/tag/getTag",
        type: "GET",
        dataType: "text",
        success: function (data) {
            $("#tag").html(data)
            $("#tag1").html(data)
        }
    })

    $.ajax({
        url: "/data/getTagMovie",
        type: "GET",
        dataType: "json",
        success: function (data) {
            for (i=0;i<data.movieId.length;i++){
                $("#tagMovieList").html(
                    $("#tagMovieList").html() +
                    "<tr><th>" + data.movieId[i] + "</th><th>" +
                    data.title[i] + "</th><th>" + "</th></tr>"
                );
            }
        },
        error: function () {
            alert("传递失败");
        }
    })

})
