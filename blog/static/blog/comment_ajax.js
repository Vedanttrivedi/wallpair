var btn = document.querySelector("#submit");
btn.addEventListener("click",bhide);
function bhide()
{
  let input = document.querySelector("#input");
  if(input.value.trim()!="")
  {
    $.ajax(
    {
      type:"POST",
      url:"/comments/",
      data:
      {
      'qid':parseInt(document.querySelector("#pk").value),
      'author':$("#author").val(),
      'content':$("#input").val(),
      'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
    }
  }
    )
var main = document.querySelector("#div");
var div = document.createElement("div");
var span = document.createElement('span');
var span2 = document.createElement('span2');

var img  = document.createElement('img');
var p = document.createElement('p');
var date = document.createElement('p');
span.style.float="right";
span.style.color="red";
span2.innerText = document.querySelector("#author").value;
span2.style.marginLeft="3px";
span.appendChild(span2);
img.src=document.querySelector("#imageurl").innerText;
img.style.width="50px";
img.style.borderRadius="50%";
p.style.fontSize="14px";
p.style.textTransform="capitalize";
p.style.color="deeppink";
date.style.float="right";
p.innerText = document.querySelector("#input").value;
var d = Date();
var r = d.toString();
date.innerText = r.slice(4,15);
div.appendChild(p);
console.log(span);
div.appendChild(img);
div.appendChild(span);
div.appendChild(date);
main.nextElementSibling=div;
console.log(div);
input.value="";

}
else
{
  alert('comment cannot be empty');
}
}
