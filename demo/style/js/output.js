function toggleOther(e){
	var the_form=document.getElementById('big_form');
	if(the_form.resolution.value=="OTHER") {
		the_form.custom_resolution.disabled=false;
		the_form.custom_resolution.focus()
	} else
		the_form.custom_resolution.disabled=true;
}