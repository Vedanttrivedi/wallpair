    var btn1 = document.querySelector(".img8");
    btn1.addEventListener('click',add);
     btn1.addEventListener('click',my);
     var btn3 = document.querySelector(".img10");
    btn3.addEventListener('click',add2);
     btn3.addEventListener('click',my);
var audio1 = document.getElementById("sound1");
var audio2 = document.getElementById("sound2");
        var l1 = parseInt(document.querySelector("#l1").innerText);
        var l2 = parseInt(document.querySelector("#l2").innerText);
        let a=0,b=0,c=0,d=0;
        if(l1==0)
        {
          var img =  document.querySelector(".img8");
          img.src="/static/blog/bbbb.png";
        }
        else
        {
            var img =  document.querySelector(".img8");
          img.src="/static/blog/aaa.png";
        }
         if(l2==0)
        {
          var img =  document.querySelector(".img10");
          img.src="/static/blog/bbbb.png";
        }
        else
        {
            var img =  document.querySelector(".img10");
          img.src="/static/blog/aaa.png";
        }

   function add()
     {
        if(l1==0)
        {
        audio1.play();
          l1=1;
          var img =  document.querySelector(".img8");
          img.src="/static/blog/aaa.png";
          img.style.transition="0.8s ease-out";
          var x  = document.querySelector("#l1d").innerText;
          document.querySelector("#l1d").innerText = parseInt(parseInt(x)+1);
          if(l2==1)
          {
            parseInt(document.querySelector("#l2d").innerText =document.querySelector("#l2d").innerText-1);
            l2=0;
            var img =  document.querySelector(".img10");

          img.src="/static/blog/bbbb.png";
          }
        }
        else if(l1==1)
        {
          var img =  document.querySelector(".img8");

          img.src="/static/blog/bbbb.png";
          img.style.transition="0.8s ease-out";
        var x  = document.querySelector("#l1d").innerText;
         document.querySelector("#l1d").innerText= parseInt(x)-1;
        
         l1=0;
         }
    }
    function add2()
      {
        if(l2==0)
        {
          audio1.play();
          var img =  document.querySelector(".img10");

          img.src="/static/blog/aaa.png";
          img.style.transition="0.8s ease-out";
          var x  = document.querySelector("#l2d").innerText;
          document.querySelector("#l2d").innerText= parseInt(x)+1;
           if(l1==1)
          {
            var img =  document.querySelector(".img8");
            img.src="/static/blog/bbbb.png";
            document.querySelector("#l1d").innerText = parseInt(document.querySelector("#l1d").innerText-1);
            l1=0;
          }
         
          
          l2=1;
        }
        else if(l2==1)
        {
         var img =  document.querySelector(".img10");

          img.src="/static/blog/bbb.png";
          img.style.transition="0.8s ease-out";
         var x  = document.querySelector("#l2d").innerText;
          document.querySelector("#l2d").innerText= parseInt(x)-1;
          document.querySelector("#img2").style.transform='rotate(-360deg)';
          document.querySelector("#img2").style.transition='1.5s ease-out';

         l2=0;
         }
    }

      function done(data,textStatus){
        /*var ele = document.querySelector("#like").nextElementSibling;
        ele.nextElementSibling.innerText=data;+*/
        //console.log(data);
      }

function my()
{
        $.ajax({
          type:"POST",
          url:'/votes/'+$("#pk").val(),
          data:{
            'pk':$("#pk").val(),
            'l1':l1,
            'l2':l2,
            'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
          },
          success:done,
          dataType:'html'

        })

    }