var frame_border=0;
var frame_width=230;
var frame_height=370;


var ARROW_UP = 38;
var ARROW_DOWN = 40;

var target=null;
var comp;
var startX=null;
var startY=null;
var newX,relX;
var newY,relY;
var frame_top;
var frame_left;
var cur_top, cur_left, cur_width, cur_height;
var info_form;
var overlay;
var old_cur_top;
var old_cur_left;

var running = false;


function setSelectionConstants(){
	target=document.getElementById('preview');
	comp=document.getElementById('selection');
	overlay=document.getElementById('overlay');
	info_form=document.getElementById('big_form');

	frame_top=findPosY(target)+frame_border;
	frame_left=findPosX(target)+frame_border;


	cur_top=frame_border;
	cur_left=frame_border;
	cur_width=frame_width;
	cur_height=frame_height;
	relX=0;
	relY=0;
	
	applyNewCoords();	
	
	/*Hack to get valid xhtml strict*/
	document.getElementById('top_coord').autocomplete='off';
	document.getElementById('left_coord').autocomplete='off';
	document.getElementById('height_coord').autocomplete='off';
	document.getElementById('width_coord').autocomplete='off';
}



function getRelX(absX) {
	return absX - frame_left;
}

function getRelY(absY) {
	return absY - frame_top;
}

function startselection(e){
	if (running) {return;} else {running=true;} /*Only start selection, if endselection has been called for the previous one*/

	frame_top=findPosY(target)+frame_border;
	frame_left=findPosX(target)+frame_border;
	
	if(mozilla) {	
		startX=e.pageX;
		startY=e.pageY;
	} else {
		e = window.event;
		startY=e.clientY + document.documentElement.scrollTop;
		startX=e.clientX + document.documentElement.scrollLeft;
	}

	

	newX=startX+1;
	newY=startY+1;
	
	comp.style.backgroundPosition=frame_left+unit+" "+frame_top+unit;
	
		
	if(getRelX(startX) < 0) { startX=frame_left; }
	if(getRelY(startY) < 0) { startY=frame_top; }
	if(getRelX(startX) > frame_width) { startX = frame_left + frame_width; }
	if(getRelY(startY) > frame_height) { startY = frame_top + frame_height; }
	updateCurSelectionCoords();
	updateSelectionInfo();
	document.body.onmousemove=changeselection;
    document.body.onmouseup=endselection;
    
}
function endselection(e){
	running=false;
	
	document.body.onmousemove=null;
	document.body.onmouseup=null;
	updateSelectionInfo();
}

function changeselection(e) {

	if(mozilla) {	
		newX=e.pageX;
		newY=e.pageY;
	} else {
		e = window.event;
		newY=e.clientY + document.documentElement.scrollTop;
		newX=e.clientX + document.documentElement.scrollLeft;
	}
	
	updateCurSelectionCoords();
	
	/*Commenting out the next line will speed up the script by almost 50%, 
	but the boxes will not show the coordinates as they change..*/
/*	alert("Gonna update selection info");*/
	updateSelectionInfo();
    
}

function updateCurSelectionCoords(){
	old_cur_top=cur_top;
	old_cur_left=cur_left;
    
    
	if(getRelX(newX) < 0) { newX=frame_left; }
	if(getRelY(newY) < 0) { newY=frame_top; }
	if(getRelX(newX) > frame_width) { newX=frame_left+frame_width; }
	if(getRelY(newY) > frame_height) { newY=frame_top+frame_height; }
    
	/*Bounds check*/
	if(newX<startX) {
		cur_left=newX;
		cur_width=startX-newX;
	} else {
		cur_left=startX;
		cur_width=newX-startX;
	}
	
	/*Bounds check*/
	if(newY<startY) {
		cur_top=newY;
		cur_height=startY-newY;
	} else {
		cur_top=startY;
		cur_height=newY-startY;
	}
	/*alert(cur_height);*/
    
    /*Let's not do anything of old_left==cur_left*/
	if(old_cur_left!=cur_left) {
		relX=getRelX(cur_left);
		overlay.style.paddingLeft=relX+unit;
		overlay.style.width=frame_width-relX+unit;
	}
	
	/*Let's not do anything of old_top==cur_top*/
	if(old_cur_top!=cur_top) {
		relY=getRelY(cur_top);
		overlay.style.paddingTop=relY+unit;
		overlay.style.height=frame_height-relY+unit;
	}

	comp.style.backgroundPosition=(-relX) +unit+" "+(-relY)+unit;
	
	comp.style.width=cur_width+unit;
	comp.style.height=cur_height+unit;

}

/*Updates the boxes with the size and location info*/
function updateSelectionInfo() {
	info_form.width_coord.value=cur_width;
	info_form.height_coord.value=cur_height;
	info_form.top_coord.value=relY;
	info_form.left_coord.value = relX;
	
}

function changeTop(e,amount){
	if(e.keyCode == ARROW_DOWN) {
		info_form.top_coord.value=relY+amount;
	} else if (e.keyCode == ARROW_UP) {
		info_form.top_coord.value=relY-amount;
	}
	applyNewCoords();
}
function changeWidth(e,amount){
	if(e.keyCode == ARROW_DOWN) 
		info_form.width_coord.value=cur_width+amount;
	else if (e.keyCode == ARROW_UP)
		info_form.width_coord.value=cur_width-amount;
		
	applyNewCoords();
}
function changeHeight(e,amount){
	if(e.keyCode == ARROW_DOWN) 
		info_form.height_coord.value=cur_height+amount;
	else if (e.keyCode == ARROW_UP) 
		info_form.height_coord.value=cur_height-amount;
	
	applyNewCoords();
}
function changeLeft(e,amount){
	if(e.keyCode == ARROW_DOWN) 
		info_form.left_coord.value=relX+amount;
	else if (e.keyCode == ARROW_UP) 
		info_form.left_coord.value=relX-amount;
	
	applyNewCoords();
}

function applyNewCoords() {
	startY = frame_top + parseInt(info_form.top_coord.value);
	startX = frame_left + parseInt(info_form.left_coord.value);
	
	if(getRelX(startX) < 0 || isNaN(startX)) { startX=frame_left; }
	if(getRelY(startY) < 0 || isNaN(startY)) { startY=frame_top; }
	if(getRelX(startX) > frame_width) { startX = frame_left + frame_width; }
	if(getRelY(startY) > frame_height) { startY = frame_top + frame_height; }

	newX = startX + parseInt(info_form.width_coord.value);
	newY = startY + parseInt(info_form.height_coord.value);
	
	if(isNaN(newX)) newX=startX;
	if(isNaN(newY)) newY=startY;
	updateCurSelectionCoords();
	updateSelectionInfo();
}
