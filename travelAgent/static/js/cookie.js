function getCookie(name) {
    var name = escape(name);
    //Read the cookie property, which returns all cookies for the document
    var allcookies = document.cookie;
    //Find the starting position of the cookie named name
    name += "=";
    var pos = allcookies.indexOf(name);
    //If a cookie with that name is found, its value is extracted and used
    if (pos != -1) {                                             //If pos is -1, the search for "version=" fails
        var start = pos + name.length;                  //The position where the cookie value starts
        var end = allcookies.indexOf(";", start);        //Search for the first ";" starting from the cookie value Where the cookie value ends
        if (end == -1){
           end = allcookies.length;
        }         //If the end value is -1, there is only one cookie in the cookie list
        var value = allcookies.substring(start, end); //Extract the value of the cookie
        return (value);                           //Decoding to it
    }
    else
    {
       return ""; //Search failed. Empty string returned
    }
}

function setCookie(name, value, hours, path) {
    var name = escape(name);
    var value = escape(value);
    var expires = new Date();
    expires.setTime(expires.getTime() + hours * 3600000);
    path = path == "" ? "" : ";path=" + path;
    _expires = (typeof hours) == "string" ? "" : ";expires=" + expires.toUTCString();
    document.cookie = name + "=" + value + _expires + path;
}

function clearCookie(name){
    setCookie(name,"",-1);

}
