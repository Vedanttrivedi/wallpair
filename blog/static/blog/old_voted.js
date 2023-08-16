 var l1=0;
var dl1=0;
var l2=0;
var dl2=0;
var pk = 0;
var user = document.querySelector("#xox").innerHTML;
var img1per =document.querySelectorAll(".img1per");
var img2per =document.querySelectorAll(".img2per");

for(var i=0;i<img1per.length;i++)
{
  var like1 = img1per[i].previousElementSibling.children[2].innerText;
  var dlike1 = img1per[i].previousElementSibling.children[5].innerText;
  var like2 = img1per[i].parentNode.parentNode.children[2].children[1].children[2].innerText;
  var dlike2 = img1per[i].parentNode.parentNode.children[2].children[1].children[5].innerText;
  console.log((parseInt(like1) + parseInt(dlike2) * 100 ) / (parseInt(like1) + parseInt(dlike2)+parseInt(dlike1)+parseInt(like2)));
  let y = ((parseInt(like1) + parseInt(dlike2)) * 100 ) / (parseInt(like1) + parseInt(dlike2)+parseInt(dlike1)+parseInt(like2));
  img1per[i].innerText = parseInt(y)+ '%';
}

for(var i=0;i<img2per.length;i++)
{
  var like2 = img2per[i].previousElementSibling.children[2].innerText;
  var dlike2 = img2per[i].previousElementSibling.children[5].innerText;
  var like1 = img2per[i].parentNode.parentNode.children[1].children[1].children[2].innerText;
  var dlike1 = img2per[i].parentNode.parentNode.children[1].children[1].children[5].innerText;
  let y = ((parseInt(like2) + parseInt(dlike1)) * 100 ) / (parseInt(like1) + parseInt(dlike2)+parseInt(dlike1)+parseInt(like2));
  img2per[i].innerText = parseInt(y)+ '%';
}
for(var i=0;i<img1per.length;i++)
{
  let y = parseInt(img1per[i].innerText);
  let z = parseInt(img2per[i].innerText);
  if(y > z)
  {
    img1per[i].style.color="green";
    img2per[i].style.color="red";

  }
  else if(z>y)
  {
    img1per[i].style.color="red";
    img2per[i].style.color="green";

  }

}
//document.querySelector("#img1").style.transform='rotate(360deg)';
          //document.querySelector("#img1").style.transition='1.5s ease-out';
        function add(cur)
        {
            if(parseInt(user)==1)
            {
              var user_likes1 = cur.nextElementSibling.innerText;

        console.log(cur.parentNode.parentNode.children[0]);

         var main_likes1 = cur.nextElementSibling.nextElementSibling.innerText;

         if(parseInt(user_likes1)==0)
         {
          l1 = 1;
          cur.src="/static/blog/a.png";
          cur.parentNode.parentNode.children[0].style.transform="rotate(360deg)";
          cur.nextElementSibling.innerText = parseInt(1);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) +1;
          var user_likes2 = cur.parentNode.parentNode.parentNode.children[2].children[1].children[1].innerText;
          var main_likes2 = cur.parentNode.parentNode.parentNode.children[2].children[1].children[2].innerText;
          //for userlike2
          if(parseInt(user_likes2)==1)
          {
            l2=0;
            cur.parentNode.parentNode.parentNode.children[2].children[1].children[1].innerText = parseInt(0);
            cur.parentNode.parentNode.parentNode.children[2].children[1].children[2].innerText = parseInt(cur.parentNode.parentNode.parentNode.children[2].children[1].children[2].innerText)-1;
            cur.parentNode.parentNode.parentNode.children[2].children[1].children[0].src="/static/blog/b.png";
          }
          //for userdislike1
          var user_dislikes2 = cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText;
          var main_dislikes2 = cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText;
           if(parseInt(user_dislikes2)==1)
          {
            dl1=0;
            cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText = parseInt(0);
            cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText= parseInt(cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText)-1;
          cur.nextElementSibling.nextElementSibling.nextElementSibling.src="/static/blog/d_15.png";
          }
         }
         else
         {
          l1 = 0;
          cur.parentNode.parentNode.children[0].style.transform='rotate(-360deg)';
          cur.nextElementSibling.innerText = parseInt(0);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) -1;
         cur.src="/static/blog/b.png";
         }

        $.ajax({
          type:"GET",
          url:'/likes1/',
          data:{
            'pk':parseInt(cur.parentNode.parentNode.parentNode.children[0].innerHTML),
          },
          success:function()
          {
          }
          ,
          dataType:'html'

        })

            }
            else
            {
              document.querySelector("#link").click();
            }
        }


         function add1(cur)
        {
          if(parseInt(user)==1)
          {
              var user_dislikes1 = cur.nextElementSibling.innerText;

          var main_dislikes1 = cur.nextElementSibling.nextElementSibling.innerText;
          console.log(main_dislikes1);
          if(parseInt(user_dislikes1)==0)
         {
          dl1 = 1;
          cur.src="/static/blog/c.png";
          cur.parentNode.parentNode.children[0].style.transform='rotate(-360deg)';
          cur.nextElementSibling.innerText = parseInt(1);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) +1;
          var user_likes1 = cur.previousElementSibling.previousElementSibling.innerText;
          var main_likes1 = cur.previousElementSibling.innerText;
          //for userlike1

          if(parseInt(user_likes1)==1)
          {
            l1 = 0;
            cur.previousElementSibling.previousElementSibling.innerText = parseInt(0);
            cur.previousElementSibling.innerText = parseInt(cur.previousElementSibling.innerText)-1;
            cur.previousElementSibling.previousElementSibling.previousElementSibling.src="/static/blog/b.png";
          }
          //for userdislike2
          var user_dislikes2 =   cur.parentNode.parentNode.parentNode.children[2].children[1].children[4].innerText;
          var main_dislikes2 =   cur.parentNode.parentNode.parentNode.children[2].children[1].children[5].innerText;
           if(parseInt(user_dislikes2)==1)
          {
            dl2 = 0;
            cur.parentNode.parentNode.parentNode.children[2].children[1].children[4].innerText = parseInt(0);
            cur.parentNode.parentNode.parentNode.children[2].children[1].children[5].innerText = parseInt(cur.parentNode.parentNode.parentNode.children[2].children[1].children[5].innerText)-1;
          cur.parentNode.parentNode.parentNode.children[2].children[1].children[3].src="/static/blog/d_15.png";
          }
         }
         else
         {
          dl1 = 0;
          cur.src="/static/blog/d_15.png";
           cur.parentNode.parentNode.children[0].style.transform='rotate(360deg)';
          cur.nextElementSibling.innerText = parseInt(0);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) -1;
         }
          $.ajax({
          type:"GET",
          url:'/dlikes1/',
          data:{
            'pk':parseInt(cur.parentNode.parentNode.parentNode.children[0].innerHTML),
          },
          success:function()
          {
          }
          ,
          dataType:'html'

        })
          }
          else
          {
            document.querySelector("#link").click();
          }
        }


function add2(cur)
  {
   if(parseInt(user)==1)
   {
var user_likes2 = cur.nextElementSibling.innerText;

         var main_likes2 = cur.nextElementSibling.nextElementSibling.innerText;

         if(parseInt(user_likes2)==0)
         {
          l2 = 1;
          cur.src="/static/blog/a.png";
          cur.nextElementSibling.innerText = parseInt(1);
           cur.parentNode.parentNode.children[0].style.transform='rotate(360deg)';
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) +1;
          var user_likes1 = cur.parentNode.parentNode.parentNode.children[1].children[1].children[1].innerText;
          var main_likes1 = cur.parentNode.parentNode.parentNode.children[1].children[1].children[2].innerText;
          //for userlike1
          if(parseInt(user_likes1)==1)
          {
            l1=0;
            cur.parentNode.parentNode.parentNode.children[1].children[1].children[1].innerText = parseInt(0);
            cur.parentNode.parentNode.parentNode.children[1].children[1].children[2].innerText= parseInt(cur.parentNode.parentNode.parentNode.children[1].children[1].children[2].innerText)-1;
          cur.parentNode.parentNode.parentNode.children[1].children[1].children[0].src="/static/blog/b.png";
          }
          //for userdislike2
          var user_dislikes2 = cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText;
          var main_dislikes2 = cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText;
           if(parseInt(user_dislikes2)==1)
          {
            dl2=0;
            cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText = parseInt(0);
            cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText= parseInt(cur.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.innerText)-1;
            cur.nextElementSibling.nextElementSibling.nextElementSibling.src="/static/blog/d_15.png";
          }
         }
         else
         {
          l2 = 0;
           cur.parentNode.parentNode.children[0].style.transform='rotate(-360deg)';
          cur.nextElementSibling.innerText = parseInt(0);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) -1;
          cur.src="/static/blog/b.png";
         }
      $.ajax({
          type:"GET",
          url:'/likes2/',
          data:{
            'pk':parseInt(cur.parentNode.parentNode.parentNode.children[0].innerHTML),
          },
          success:function()
          {
          }
          ,
          dataType:'html'

        })
   }
   else
   {
    document.querySelector("#link").click();
   }

  }


 function add3(cur)
  {
              if(parseInt(user)==1)
              {
                  var user_dislikes2 = cur.nextElementSibling.innerText;

          var main_dislikes2 = cur.nextElementSibling.nextElementSibling.innerText;

          if(parseInt(user_dislikes2)==0)
         {
          dl2 = 1;
           cur.parentNode.parentNode.children[0].style.transform='rotate(-360deg)';
          cur.src="/static/blog/c.png";
          cur.nextElementSibling.innerText = parseInt(1);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) +1;
          var user_likes2 = cur.previousElementSibling.previousElementSibling.innerText;
          var main_likes2 = cur.previousElementSibling.innerText;
          //for userlike2

          if(parseInt(user_likes2)==1)
          {
            l2 = 0;
            cur.previousElementSibling.previousElementSibling.innerText = parseInt(0);
            cur.previousElementSibling.innerText = parseInt(cur.previousElementSibling.innerText)-1;
            cur.previousElementSibling.previousElementSibling.previousElementSibling.src="/static/blog/b.png";
          }
          //for userdislikes1
          var user_dislikes1 =   cur.parentNode.parentNode.parentNode.children[1].children[1].children[4].innerText;
          var main_dislikes1 =  cur.parentNode.parentNode.parentNode.children[1].children[1].children[5].innerText;
           if(parseInt(user_dislikes1)==1)
          {
            dl1 = 0;
            cur.parentNode.parentNode.parentNode.children[1].children[1].children[4].innerText = parseInt(0);
            cur.parentNode.parentNode.parentNode.children[1].children[1].children[5].innerText = parseInt(cur.parentNode.parentNode.parentNode.children[1].children[1].children[5].innerText)-1;
            cur.parentNode.parentNode.parentNode.children[1].children[1].children[3].src="/static//blog/d_15.png";
          }
         }
         else
         {
          dl2 = 0;
          cur.src="/static/blog/d_15.png";
           cur.parentNode.parentNode.children[0].style.transform='rotate(-360deg)';
          cur.nextElementSibling.innerText = parseInt(0);
          cur.nextElementSibling.nextElementSibling.innerText = parseInt(cur.nextElementSibling.nextElementSibling.innerText) -1;
         }

                    $.ajax({
          type:"GET",
          url:'/dlikes2/',
          data:{
            'pk':parseInt(cur.parentNode.parentNode.parentNode.children[0].innerHTML),
          },
          success:function()
          {
          }
          ,
          dataType:'html'

        })
              }
              else
              {
                document.querySelector("#link").click();
              }
  }

function my(cur)
{
  if(parseInt(user)==1)
  {

      var pk = parseInt(cur.parentNode.parentNode.parentNode.children[0].innerHTML);
      console.log(pk);
        $.ajax({
          type:"GET",
          url:'/votes1/',
          data:{
            'pk':pk,
            'l1':l1,
            'dl1':dl1,
            'l2':l2,
            'dl2':dl2,
            'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
          },
          success:function()
          {
            //console.log('hello');
          }
          ,
          dataType:'html'

        })
  }
  }