// from fuzzywuzzy import process
// from fuzzywuzzy import fuzz
//import fuzzywuzzy from './chat'


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
       //  var hours = date.hours;
       //  print(hours)
       //  var msg1 = msg.time.split(" ")
       //  var b = msg1[1]
       //  var t = b.split(":")
       //  var time1 = t[0]
        // console.log("time = " + time)
        if (typeof msg.time !== "undefined") {
            var n = msg.time;
        } else {
            var n = date;
        }
        var username = load_username()
        //staff侧人工回复
        var content =
            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            msg.name +
            '</b><p>' +
            msg.message +
            '</p>'
            + ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';
        //当前用户，但不用自动回复
        if (username == msg.name) {
            //print(msg.time)
            content =
                '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
               /////////////////
                 + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 +n+
                 '</p>' +
                 /////////////////
                '</span></div>' +
                '</div></div>';

            //每次用户发信息，都
        }

        //用户出发关键词，staff侧自动回复
        //'When staff work'
        if (username == msg.name && 'When staff work?' == msg.message) {
        // if (username == msg.name && fuzz.ratio('When staff work', msg.message)>20){
             var content =
             '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
                 /////////////////
                 + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 +n+
                 '</p>' +
                 /////////////////
                '</span></div>' +
                '</div></div>' +

            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            'Auto Reply' +
            '</b><p>' +
            'Staff work between 9am-10pm' +
            '</p>' +
                 ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';
        }

        //link order page
        //'How to check order status'
         if (username == msg.name && 'How to check order status?' == msg.message) {
             var content =
             '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
              /////////////////
                 + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 +n+
                 '</p>' +
                 /////////////////
                '</span></div>' +
                '</div></div>' +

            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            'Auto Reply' +
            '</b><p>' +
            'You can check order status inside ' +
                 '<a href="http://127.0.0.1:5000/order_list">ORDERS</a>'+
                 ' page' +
            '</p>' +
           ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';
        }

         //超出时间 staff have go home
          if (username == msg.name && (((n.split(' '))[1]).split(':')[0] < 9  ) && 'When staff work?' != msg.message && 'How to check order status?' != msg.message && 'Where to check my Favorites?' != msg.message &&  'How to contact Digital Beans for further cooperation?' != msg.message) {
             var content =
             '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
                 /////////////////
                 + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 +n+
                 '</p>' +
                 /////////////////
                '</span></div>' +
                '</div></div>' +

            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            'Auto Reply' +
            '</b><p>' +
            'Staff work during 9am-10pm' +
            '</p>'+ '<p>'+
                 'Our staff will contact you ASAP later'
                 + '</p>'+ '<p>'+
                 'Auto Reply is available for particular quations:' +

            '</p>' +
                 ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';
        }

          //link Favorites
          //'Where to check my Favorites'
         if (username == msg.name && 'Where to check my Favorites?' == msg.message) {
             var content =
             '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b>' + '<p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
                 /////////////////
                 + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 +n+
                 '</p>' +
                 /////////////////
                '</span></div>' +
                '</div></div>' +

            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            'Auto Reply' +
            '</b><p>' +
                 'You can check your Favorites inside '+
                 '<a href="http://127.0.0.1:5000/favourites">FAVORITES</a>'+
                 ' page' +
             //  '<button onclink="mylink(this)" value="http://127.0.0.1:5000/favourites">Favoritesss</button>'
            '</p>' +
                 ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
            '</div></div>';
        }

          //link Contact us
          //'Where to contact with Digital Benas'
         if (username == msg.name && 'How to contact Digital Beans for further cooperation?' == msg.message) {
             var content =
             '<div class="row">' +

                '<div class="col"></div>' +
                '<div class="col"></div>' +
                // '<div class="col-sm">'+
                '<div class="alert alert-success alert-shadow col-5" style="margin-right: 2%; background: rgba(67,227,203,0.4)">' +
                '<b style="color:#157" class="left">' +
                msg.name +
                '</b><p style="text-align: right; color: black">' +
                msg.message +
                '</p>'
                 /////////////
                  + '<p style="text-align: right">'
                 +'<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>' + '<span class="res_translate"></span>' + '<span class="time-right">' +
               '</p>'
             + '<p style="text-align: right; color: grey" >'
                 + n +
                 '</p>' +
                 /////////////
                '</span></div>' +
                '</div></div>' +

            '<div class="row">' +
            // '<div class="col-sm">'+
            '<div class="alert alert-shadow col-5" style="margin-left: 2%; background: rgb(124,168,246, 0.4)">' +
            '<b style="color:#734" class="right">' +
            'Auto Reply' +
            '</b><p>' +
                 'You can contact with Digital Beans for further cooperation inside '+
                 '<a href="http://127.0.0.1:5000/contactUs">CONTACT US</a>'+
                 ' page' +
             //  '<button onclink="mylink(this)" value="http://127.0.0.1:5000/favourites">Favoritesss</button>'
            '</p>' +
                 ////////////////
              '<p>' +
                 `<button class="btn btn-primary"  onclick=Translate(event)>Translate</button>` + '<span class="res_translate"></span>' + '<span class="time-right">' +
             '</p>' +
                 '<p style="color: grey">'+
                  n +
                 '</p>'+
                 /////////////////
            '</span></div>' +
            '<div class="col"></div>' +
            '<div class="col"></div>' +
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
function mylink(link) {
    window.location.href="http://127.0.0.1:5000/favourites";
    console.log(link.value);
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





