/*
Copyright (C) 2005: Mikko Virkkilä (mvirkkil@cc.hut.fi)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/
var cont_height = 100;
var cont_padding = 10;
var float_half_height=6;
var floater;
var container_top;
var cont;
var stat;
var origY;
var unit;


/*The following function is from QuirksMode, hence not under the GPL*/
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

/*The following function is from QuirksMode, hence not under the GPL*/
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
		/*alert('Mozilla');*/
		mozilla=true;
		unit='px'; /*Though mozilla gladly accepts 'px;' khtml doesn't so we just use 'px'*/
	} else {
		/*alert('IE');*/
		mozilla=false;
		unit='';
	}
	
    document.getElementById(toSet).style.top=cont_height-50-(getCurLevel(toGet)/2)-float_half_height+unit;
    
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
	
}

function changelevel(e) {
	var newY;
	if (mozilla) { 
		newY=e.pageY-container_top;
	} else {
		e = window.event;
		newY=e.clientY + document.documentElement.scrollTop - container_top;
	}
	if(newY< 0) {newY=0;}
	if(newY>cont_height) {newY=cont_height;}
	stat.value=(100-2*newY);
	floater.style.top=newY-float_half_height+unit;
}

function getCurLevel(toGet){
	var result=document.getElementById(toGet).value;
	/*var val=result.substr(0, result.length-1);*/


	return result;
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
