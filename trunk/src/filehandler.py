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
	
	def getFilenames(self):
		return self.openfiles.keys()
	
	def exists(self, filename):
		return self.openfiles.has_key(filename)
		
	def createFile(self,filename):
		file,path=tempfile.mkstemp('','websane_')
		self.openfiles[filename]=(file,path)
		return file
		
	def openFile(self,filename):
		f,p=self.openfiles[filename]
		if not f.closed:
			print "The file hasn't been closed!"
			raise IOError
		else
			self.openfiles[filename]=(open(p),p)
			return self.openfiles[filename][0]

	def deleteFile(self, filename):
		f,p=self.openfiles[filename]
		if not f.closed:
			print "Warnign: The file hasn't been closed, unlinking anyway"
		os.unlink(p)
		del self.openfiles[filename]
	
	def deleteAllFiles(self):
		for f,p in self.openfiles:
			deleteFile(p)
		self.openfiles.clear()

def main():
	print "No tests"
	
	
	
if __name__ == '__main__':
	main()

