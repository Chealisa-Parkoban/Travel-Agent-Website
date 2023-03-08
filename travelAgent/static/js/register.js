function bindCaptchaBtnClick(){
    // 这个dollar函数可以获取对应button的信息，如果是获取id，则是在双引号内加上#加id
    $("#captcha-btn").on("click", function (event){
        // this 表示的是当前函数，但是套上$() 就变成了jQuery
        var $this = $(this);
    //    点击以后要获取邮箱文本
        var email = $("input[name='email']").val();
        if (!email){
            alert("Please fill the email");
        }
        // 通过js发送网络请求，ajax，异步js和xml
        $.ajax({
            url: "/captcha",
            // url: "../views/login_handler/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                var code = res["code"]
                if (code == 200){
                    // 先得取消按钮的点击事件，防止用户进一步连续点击
                    $this.off("click");
                    // 开始倒计时
                    var countDown = 60;
                    var timer = setInterval(function (){
                        countDown = countDown -1;
                        if (countDown>0) {
                            $this.text(countDown + "second, send again");
                        }
                        else {
                            // 倒计时结束后，文字恢复并且可以重新执行点击任务
                            $this.text("Get verification code");
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时，记得要清除计时器，否则会一直执行
                            clearInterval(timer);
                        }
                    }, 1000);

                    alert("Send verification code successfully")
                }
                else {
                    alert(res['message'])
                }
            }
        })
    })
}

// $等网页文档所有元素都加载完再执行
$(function (){
    bindCaptchaBtnClick();
})