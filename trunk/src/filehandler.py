#!/usr/bin/python
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

import ConfigParser
from time import time
import tempfile

class FileHandler:
	openfiles={}
	
	def exists(self, filename):
		if self.openfiles == None:
			return False
		try:
			self.openfiles[filename]
			return True
		except KeyError:
			return False
		
		
	def createFile(self,filename):
		file=tempfile.TemporaryFile()
		self.openfiles[filename]=file
		return file
		
	def loadFile(self,filename):
		f=self.openfiles[filename]
		f.seek(0)
		return f		

	def deleteFile(self, filename):
		self.openfiles[filename].close()
		del self.openfiles[filename]
	
def main():
	print "No tests"
	
	
	
if __name__ == '__main__':
	main()

