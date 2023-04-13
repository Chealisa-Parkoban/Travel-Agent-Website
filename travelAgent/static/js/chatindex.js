//translate function
function Translate(event) {
    console.log(event.target)
    var previous = event.target.previousElementSibling.innerText
    var next = event.target.nextElementSibling

    var appid = '20230228001579285';
    var key = 'i_i50GKeYlqZOVY7Q8HS';
    var salt = (new Date).getTime();
    var from = 'auto';
    var to = 'en';

    //翻译
    // $("#goTran").click(function(){
    var query = previous;
    var str1 = appid + query + salt + key;
    var sign = md5(str1);
    $.ajax({
        url: 'http://api.fanyi.baidu.com/api/trans/vip/translate',
        type: 'get',
        dataType: 'jsonp',
        data: {
            q: query,
            appid: appid,
            salt: salt,
            from: from,
            to: to,
            sign: sign
        },
        success: function (data) {
            var res = data.trans_result[0].dst;
            // $("#result")[0].innerHTML=res;
            console.log(res);
            event.target.nextElementSibling.innerText = res

        }
    });
}

// add message to the chat zone
async function add_messages(msg, scroll) {
    console.log(msg.name)
    if (typeof msg.name !== "undefined") {
        var date = dateNow();

        if (typeof msg.time !== "undefined") {
            var n = msg.time;
        } else {
            var n = date;
        }
        var username = load_username()

        var content =
            '<div class="row">' +


            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%">' +
            '<b style="color:#734" class="right">' +
            msg.name +
            '</b><p>' +
            msg.message +
            '</p>' + `<button class="btn btn-primary" onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
            n +
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';

        if (username == msg.name) {
            content =
                '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>' + '<button class="btn btn-primary" onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-left">' +
                n +
                '</span></div>' +
                '</div></div>';
        }
        // update div
        var messageDiv = document.getElementById("messages");
        messageDiv.innerHTML += content;
    }

    if (scroll) {
        scrollSmoothToBottom("messages");
    }
}

function load_username() {
    return $('#username').html()
}

function load_name() {
    return $('#name').html()
}

async function load_messages() {
    return await fetch("/chat/get_messages_of_user")
        .then(async function (response) {
            return await response.json();
        })
        .then(function (text) {
            console.log(text);
            return text;
        });
}

$(function () {
    $(".msgs").css({height: $(window).height() * 0.7 + "px"});

    $(window).bind("resize", function () {
        $(".msgs").css({height: $(window).height() * 0.7 + "px"});
    });
});

function scrollSmoothToBottom(id) {
    var div = document.getElementById(id);
    $("#" + id).animate(
        {
            scrollTop: div.scrollHeight - div.clientHeight,
        },
        500
    );
}

function dateNow() {
    var date = new Date();
    var aaaa = date.getFullYear();
    var gg = date.getDate();
    var mm = date.getMonth() + 1;

    if (gg < 10) gg = "0" + gg;

    if (mm < 10) mm = "0" + mm;

    var cur_day = aaaa + "-" + mm + "-" + gg;

    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();

    if (hours < 10) hours = "0" + hours;

    if (minutes < 10) minutes = "0" + minutes;

    if (seconds < 10) seconds = "0" + seconds;

    return cur_day + " " + hours + ":" + minutes;
}

console.log("http://" + document.domain + ":" + location.port)
var socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on("connect", async function () {
    console.log("connect")
    var username = load_username();
    if (username != "") {
        socket.emit("event", {
            message: username + " just connected to the server!",
            connect: true,
        });
    }
    $("#sendBtn").on("click", async function (e) {
        e.preventDefault();

        // get input from message box
        let msg_input = document.getElementById("msg");
        let user_input = msg_input.value;
        if (user_input == "") {
            alert("Please input something then send.");
            return false;
        }
        let user_name = load_username();
        let name = load_name();
        console.log(msg_input)
        // clear msg box value
        msg_input.value = "";

        // send message to other users
        socket.emit("event", {
            message: user_input,
            username: user_name,
            name: name,
        });

        return false;
    });
});
socket.on("disconnect", async function (msg) {
    var username = load_username()
    socket.emit("event", {
        message: username + " just left the server...",
    });
});
socket.on("message response", function (msg) {
    add_messages(msg, true);
});

window.onload = async function () {
    var msgs = await load_messages();
    for (i = 0; i < msgs.length; i++) {
        scroll = false;
        if (i == msgs.length - 1) {
            scroll = true;
        }
        add_messages(msgs[i], scroll);
    }

    let name = await load_name();
    if (name != "") {
        $("#login").hide();
    } else {
        $("#logout").hide();
    }
};





