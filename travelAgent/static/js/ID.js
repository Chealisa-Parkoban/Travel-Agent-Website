function setID(el) {
    set_id = $(el).attr("set_id");
    console.log("set id = " + set_id)
    $.ajax({
        type: "POST",
        url: "/transport_setID",
        dataType:"JSON",
        data: {
            "set_id": set_id
        },//提交的数据
        success: function (res) {
            console.log("传送set id数据成功");

        },
        error: function () {
            alert("向后台传输set id数据出错");
        }
    })

}