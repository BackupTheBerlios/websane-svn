# -*- coding: UTF8 -*-
# Copyright (C) 2005: Mikko Virkkilä
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


from xml.dom.minidom import parse
import ConfigParser
from time import time

class XMLHandler:
	input_radio={	"imgtype":"COLOR",
					"rotation":"0"}

	input_text={	"brightness":"0",
					"contrast":"0",
					"custom_resolution":"0",
					"filename":"",
					"left":"20",
					"top":"50",
					"width":"100",
					"height":"200" }

	input_hidden={	"action":"" }

	input_checkbox={"before_save":"view"}

	select={		"filetype":"PNG",
					"resolution":"200"}
					
	def getDocument(self):
		return self.dom.toxml('UTF8')
	
	def setRotation(self,rottoset):
		print "Starting to change rotation"
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='rotation' and input.attributes['value'].value==rottoset:
				print "Selecting rotation"
				input.setAttribute('checked','checked')
	
	def __init__(self,filename):
		t=time()
		self.dom=parse(filename)
		for input in self.dom.getElementsByTagName('input'):
			print input.attributes['name'].value, input.attributes['value'].value

		print "Opening and parsing XML document done. Took",time()-t,"seconds."
			
			
			
			
			
			
			
			
			
			
