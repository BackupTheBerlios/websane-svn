var cont_height = 100;
var cont_padding = 10;
var float_half_height=6;
var floater;
var container_top;
var cont;
var stat;
var origY;
var unit;


function findPosX(obj)
{
	var curleft = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curleft += obj.offsetLeft
			obj = obj.offsetParent;
		}
	}
	else if (obj.x)
		curleft += obj.x;
	return curleft;
}

function findPosY(obj)
{
	var curtop = 0;
	if (obj.offsetParent)
	{
		while (obj.offsetParent)
		{
			curtop += obj.offsetTop
			obj = obj.offsetParent;
		}
	}
	else if (obj.y)
		curtop += obj.y;
	return curtop;

}













function initControl(toGet, toSet) {	
	if (window.Event) {
		mozilla=true;
		unit='px;';
	} else {
		mozilla=false;
		unit='';
	}
    document.getElementById(toSet).style.top=cont_height-getCurLevel(toGet)-float_half_height+unit;
}

function startcontrol(e, container, toUpdate){
	
	if (mozilla) { 
		origY=e.pageY;
		floater=e.target;
	} else {
		e = window.event;
		origY=e.clientY + document.documentElement.scrollTop;
		floater=e.srcElement;
	}


	cont=document.getElementById(container);
	stat=document.getElementById(toUpdate);

	document.body.onmousemove=changelevel;
	document.body.onmouseup=endcontrol;
	container_top=findPosY(cont)+cont_padding;
	cont.style.cursor='n-resize';
	/*alert(floater.style.top);*/
}

function changelevel(e) {
	var newY;
	if (mozilla) { 
        /*alert('mozilla');*/
		newY=e.pageY-container_top;
	} else {
		e = window.event;
		newY=e.clientY + document.documentElement.scrollTop - container_top;
	}
	if(newY< 0) {newY=0;}
	if(newY>cont_height) {newY=cont_height;}
	stat.value=(100-newY)+'%';
	floater.style.top=newY-float_half_height+unit;
}

function getCurLevel(toGet){
	var result=document.getElementById(toGet).value;
	var val=result.substr(0, result.length-1);


	return val;
}

function endcontrol(e){
	cont.style.cursor='default';
	document.body.onmousemove=null;
	document.body.onmouseup=null;
	cont=null;
	floater=null;
	stat=null;
	origY=null;
	
}