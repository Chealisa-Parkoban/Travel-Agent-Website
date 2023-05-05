function improve(el){
    // var image = document.getElementById("image");
    var image = $(el).attr("route");
    var id = $(el).attr("i");
    //获取最后一个.的位置
    var index= image.lastIndexOf(".");
    //获取后缀
    var ext = image.substr(index+1);
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
            // $("#"+id).attr("src", "data:image/jpg;base64," + imageData);
            $("#"+id).attr("src", "data:image/" + ext + ";base64," + imageData);
        },
        error: function () {
            alert("image 错误");
        }
    })

}