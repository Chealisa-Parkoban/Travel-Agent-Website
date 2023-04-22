function improve(){
    var image = document.getElementById("image");
    var img_route = image.getAttribute("src");
    console.log("img = " + img_route)
    $.ajax({
        type: "POST",
        url: "/improveImage",
        dataType:"JSON",
        data: {
            "img_route": img_route
        },//提交的数据
        success: function (res) {
            console.log("res结果")
            console.log(res)
            let imageData = res.image
            $("#image2").attr("src", "data:image/jpg;base64," + imageData);
        },
        error: function () {
            alert("image 错误");
        }
    })

}