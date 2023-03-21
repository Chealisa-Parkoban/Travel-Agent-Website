//table分页
var pageSize=10;  //每页显示的记录条数
var curPage=0;   //显示第curPage页
var len;         //总行数
var page;        //总页数
$(function(){
    len =$("#containerTable tr").length-1;   //去掉表头
    page=len % pageSize==0 ? len/pageSize : Math.floor(len/pageSize)+1;//根据记录条数，计算页数
    console.log("len:"+len+"page:"+page);
    document.getElementById("page").value=page;
    curPage=1;
    displayPage();//显示第一页
    $("#nextPageButton").click(function(){//下一页
        if(curPage<page){
            curPage+=1;
        }
        else{
            alert("It's the last page")
        }
        displayPage();
    });
    $("#prePageButton").click(function(){//上一页
        if(curPage>1){
            curPage-=1;
        }
        else{
            alert("It's already page one");
        }
        displayPage();
    });

});

function displayPage(){
    var begin=(curPage-1)*pageSize;//起始记录号
    var end = begin + pageSize;
    console.log("  begin:"+len+"   end:"+end);
    if(end > len ) end=len;
    $("#tdata tr").hide();
    $("#containerTable tr").each(function(i){
        if(i-1>=begin && i-1<end)//显示第page页的记录
        {
            $("#containerTable_one").show();
            $(this).show();
            document.getElementById("curPage").innerHTML=curPage;
            document.getElementById("countPage").innerHTML = len;
        }
    });

}
function pageSize2(){
    curPage=0;   //显示第curPage页
    pageSize=parseInt(document.getElementById("pageSize").value);
    len =$("#containerTable tr").length-1;   //去掉表头
    page=len % pageSize==0 ? len/pageSize : Math.floor(len/pageSize)+1;//根据记录条数，计算页数
    console.log("len:"+len+"   page:"+page);
    document.getElementById("page").value=page;
    curPage=1;
    displayPage();//显示第一页
}
//end