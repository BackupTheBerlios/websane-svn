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

'''
Todo: 

 Later:
  - It should be able to modify all settings like a dictionary

'''


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


	def hideBox(self, boxId):
		for input in self.dom.getElementsByTagName('div'):
			if input.getAttributeNode('id') != None:
				if input.attributes['id'].value==boxId:
					input.setAttribute('style',"display: none")
					return

	def setBrightness(self,brightness):
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='brightness':
				input.setAttribute('value',brightness)

	def setContrast(self,contrast):
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='contrast':
				input.setAttribute('value',contrast)


	def setBounds(self,left,top,width,height):
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='left':
				input.setAttribute('value',left)
			elif input.attributes['name'].value=='top':
				input.setAttribute('value',top)
			elif input.attributes['name'].value=='width':
				input.setAttribute('value',width)
			elif input.attributes['name'].value=='height':
				input.setAttribute('value',height)

	def setRotation(self,rottoset):
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='rotation':
				if input.attributes['value'].value==rottoset:
					input.setAttribute('checked','checked')
				elif input.getAttributeNode('checked')!=None:
					input.removeAttribute('checked')

	def setImageMode(self,mode):
		for input in self.dom.getElementsByTagName('input'):
			if input.attributes['name'].value=='imgtype':
				if input.attributes['value'].value==mode:
					input.setAttribute('checked','checked')
				elif input.getAttributeNode('checked') != None:
					input.removeAttribute('checked')

	def getDocument(self):
		return self.dom.toxml('UTF8')
	
	def updateValues(self,values):
		self.setBounds(values['left'],values['top'],values['width'],values['height'])
		self.setImageMode(values['imgtype'])
		self.setContrast(values['contrast'])
		self.setBrightness(values['brightness'])
		self.setRotation(values['rotation'])
	
	def __init__(self,filename):
		t=time()
		self.dom=parse(filename)
		#for input in self.dom.getElementsByTagName('input'):
		#	print input.attributes['name'].value, input.attributes['value'].value

		print "Opening and parsing XML document done. Took",time()-t,"seconds."
			
			
			
			
			
			
			
			
			
			
