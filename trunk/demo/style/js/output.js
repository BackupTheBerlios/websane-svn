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
function toggleOther(e){
	var the_form=document.getElementById('big_form');
	if(the_form.resolution.value=="OTHER") {
		the_form.custom_resolution.disabled=false;
		the_form.custom_resolution.focus()
	} else
		the_form.custom_resolution.disabled=true;
}
