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

import os
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
		if self.exists(filename):
			raise IOError
		file,path=tempfile.mkstemp('','websane_')
		os.close(file) #We want a file object, not a filedescriptor
		self.openfiles[filename]=path

		print "Created",filename,"as",path
		return open(path,'w+b')

		
	def loadFile(self,filename):
		return open(self.openfiles[filename])

	def deleteFile(self, filename):
		p=self.openfiles[filename]
		os.unlink(p)
		del self.openfiles[filename]
	
	def deleteAllFiles(self):
		for filename in self.openfiles.keys():
			os.unlink(self.openfiles[filename])
		self.openfiles.clear()

	def __del__(self):
		print "Deleting all scanned files"
		self.deleteAllFiles()
		print "Done"
def main():
	fh=FileHandler()
	f=fh.createFile('kissa')
	f.write('possu')
	print 'wrote possu'	
	f.close()
	print 'closed file'
	f=fh.loadFile('kissa')
	print f.read()
	f.close()
	fd.deleteFile('kissa')
	
if __name__ == '__main__':
	main()

