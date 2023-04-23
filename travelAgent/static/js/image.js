function improve(el){
    // var image = document.getElementById("image");
    var image = $(el).attr("route");
    var id = $(el).attr("i");
    // var img_route = image.getAttribute("src");
    console.log("img = " + image)
    console.log("id = " + id)
    $.ajax({
        type: "POST",
        url: "/improveImage",
        dataType:"JSON",
        data: {
            "img_route": image
        },//提交的数据
        success: function (res) {
            console.log("res结果")
            console.log(res.image)
            let imageData = res.image
            $("#"+id).attr("src", "data:image/jpg;base64," + imageData);
        },
        error: function () {
            alert("image 错误");
        }
    })

}