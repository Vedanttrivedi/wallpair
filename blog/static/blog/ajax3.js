$(function(){

    $("#search").keyup(function (){

      $.ajax({
        type: "GET",
        url:"/userlinks/",
        data:{
          'search':$("#search").val().trim(),
        },
        success: searchdone,
        dataType:'html'

      });

    });


});
function searchdone(data,textStatus,jqXHR)
{

  $("#data").html(data);
  console.log(data);
}
