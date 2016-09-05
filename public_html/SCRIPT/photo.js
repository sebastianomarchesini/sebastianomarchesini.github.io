window.onload=function(){
	if(!document.getElementById || !document.getElementsByTagName) return;
	links=document.getElementById("minipics").getElementsByTagName("a");
	for(i=0;i<links.length;i++)
    		links[i].onclick=function(){Show(this);return(false)}
}

function Show(obj){
	bigimg=document.getElementById("bigimage");
	bigimg.src=obj.getAttribute("href");
	smallimg=obj.getElementsByTagName("img")[0];
	t=document.getElementById("titolo");
	t.removeChild(t.lastChild);
	t.appendChild(document.createTextNode(smallimg.title));
}
