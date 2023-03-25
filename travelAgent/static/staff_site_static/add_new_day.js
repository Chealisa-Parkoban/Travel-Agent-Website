function addRow()
    {
    var card=document.getElementById("card");
    document.getElementById("row").appendChild(card.cloneNode(true));
    }