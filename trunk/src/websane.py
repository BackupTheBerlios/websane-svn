#!/usr/bin/python
# -*- coding: UTF8 -*-
# Copyright (C) 2005: Mikko Virkkilä (mvirkkil@cc.hut.fi)
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

import string
import sys
import cgi
from urllib import unquote
import urllib
import ConfigParser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import scanhandler
import xmlhandler
import filehandler

from time import time

#This is a constant and shouldn't be modified
mmperinch=25.4

config = ConfigParser.ConfigParser()
scanhandler = scanhandler.ScanHandler()


config.read('webserver.cfg')
extbase=config.get('general','externalbasepath')
basepath=config.get('general','webserverbase')
xmlhandler=xmlhandler.XMLHandler('../demo/demo.html')
filehandler=filehandler.FileHandler()

class ReqHandler(BaseHTTPRequestHandler):

	#Handle a http request for a file
	def do_GET(self):
		if self.path == extbase+'/':
			self.path= extbase+'/demo.html'
		try:	
			#If the path contains a ? then we should parse it and scan and stuff
			if self.path.find('?')!=-1:
				pathlist, values = self.urlParse(self.path)
				if not values.has_key('filename'):
					values['filename']='untitled'+str(int(time()))+'.'+string.lower(values['filetype'])
				self.handleActions(values)

			elif self.path.startswith(extbase+'/viewfile/'):
				path, values=self.urlParse(self.path)
				print "Looking for stored file"
				if filehandler.exists(unquote(path[-1])):
					print 'It seems the stored file exists'
					self.sendHeaders(self.getContentType(unquote(path[-1])))
					self.wfile.write( filehandler.loadFile(unquote(path[-1])).read() )
					print 'File sent'
				else:
					print "stored file not found"
					raise IOError

			elif self.path.startswith(extbase+'/storedfiles/'):
				path, values=self.urlParse(self.path)
				print "Looking for stored file"
				if filehandler.exists(unquote(path[-1])):
					print 'It seems the stored file exists'
					self.sendHeaders('application/octet-stream')
					self.wfile.write( filehandler.loadFile(unquote(path[-1])).read() )
					print 'File sent'
				else:
					print "stored file not found"
					raise IOError

			elif self.path==extbase+'/demo.html':
				self.sendHeaders('text/html; charset="UTF-8"')
				self.wfile.write(xmlhandler.getDocument())
							
			#Snap a preview image and send it directly to the browser
			elif self.path==extbase+'/snap':
				print "Taking snapshot"
				self.sendHeaders('image/png')
				scanhandler.update_preview(self.wfile)

			#Do a scan and return the image directly to the browser
			elif self.path==extbase+'/scan':
				self.sendHeaders('image/png')
				scanhandler.set_resolution(300.0)
				scanhandler.scan_and_save(self.wfile, 'PNG')
				
			#Used for debugging. Displays info about scanner.
			elif self.path==extbase+'/info':
				self.sendHeaders('text/plain')
				scanhandler.write_info(self.wfile)
			
			#We replace preview.png with the preview file.
			elif self.path==extbase+'/preview.png':
				try: 
					f=filehandler.getPreviewFile()
					close=False
				except IOError:
					f=open(basepath+self.path)
					close=True
				self.sendHeaders('image/png')
				self.wfile.write(f.read())
				if close:
					f.close()
			#If nothing special was aksed, just serve the file of the specified name
			else:
				print basepath+self.path
				f=open(basepath+self.path)
				
				if self.getContentType() == None:
					#Let's not serve unknown stuff
					self.sendHeaders('text/plain')
					f.close()
					return
					
				self.sendHeaders( self.getContentType())
				self.wfile.write(f.read())
				f.close()
		#If we cant open the file (=can't find the file) we send a 404
		except IOError:
			self.send_error(404, 'IOError')

	
	#This handles a "post" from the browser by translating the post request to a get 
	#request, which will be handled in the do_GET method.
	def do_POST(self):
		contentype=self.headers.getheader('content-type')
		if contentype != 'application/x-www-form-urlencoded':
			print 'Error: Uncexpected content-type specified in header: ',contentype
			return
		
		clen = self.headers.getheader('content-length')
		
		if clen:
			clen = string.atoi(clen)
		else:
			print 'Error: Header is missing content-length'
			return
		
		data = self.rfile.read(clen)
		self.path = '%s?%s' % (self.path, data)
		self.do_GET()
	
	#Maps extensions to mime types
	def getContentType(self,filename=None):
		if filename==None:
			filename=self.path

		extension = string.split(filename,'.')[-1]
		try:
			return config.get('mimetypes', string.lower(extension))
		except NoOptionError:
			return
	
	def sendHeaders(self, conttype):
		self.send_response(200)
		self.send_header('Content-type',conttype)
		self.end_headers()
		
	#This method is not written by me and as such is not licensed under the GPL
	#Refer to the original code for the copyright holder and license.
	def urlParse(self, url):
		""" return path as list and query string as dictionary
			strip / from path
			ignore empty values in query string
			for example:
			if url is: /xyz?a1=&a2=0%3A1
			then result is: (['xyz'], { 'a2' : '0:1' } )
			if url is: /a/b/c/
			then result is: (['a', 'b', 'c'], None )
			if url is: /?
			then result is: ([], {} )
		"""
		x = string.split(url, '?')
		pathlist = filter(None, string.split(x[0], '/'))
		d = {}
		if len(x) > 1:
			q = x[-1]                  # eval query string
			x = string.split(q, '&')
			for kv in x:
				y = string.split(kv, '=')
				k = y[0]
				try:
					v = urllib.unquote_plus(y[1])
					if v:               # ignore empty values
						d[k] = v
				except:
					pass
		return (pathlist, d)

	'''Returns true if done, false if more is needed'''
	def handleActions(self,values):
		#SNAP
		if values['action'] == 'snap':
			scanhandler.reset_settings()
			scanhandler.set_mode(values['imgtype'])
			
			scanhandler.set_brightness_and_contrast(
				string.atoi(values['brightness']),
				string.atoi(values['contrast']) )
			
			
			scanhandler.set_preview_rotation(string.atoi(values['rotation']))
			scanhandler.update_preview(filehandler.createPreviewFile())
			filehandler.doneUpdatingPreviewFile()
			self.redirect('demo.html')
		#SCAN
		elif values['action'] == 'scan':
			scanhandler.reset_settings()
			
			scanhandler.set_mode(values['imgtype'])
			
			scanhandler.set_brightness_and_contrast(
				string.atoi(values['brightness']),
				string.atoi(values['contrast']) )
			
			if values['resolution'] == 'OTHER':
				scanhandler.set_resolution(string.atof(values['custom_resolution']))
			else:
				scanhandler.set_resolution(string.atof(values['resolution']))
			
			scanhandler.set_scan_bounds_from_preview(values['left'],values['top'],values['width'],values['height'],values['rotation'])
			
			if values.has_key('before_save'):
				if values['before_save']=='view':
					scanhandler.scan_and_save(filehandler.createFile(values['filename']), values['filetype'])
					xmlhandler.setFiles(filehandler.getFilenames())
					self.redirect('viewfile/'+values['filename'])	
					return			

			scanhandler.scan_and_save(filehandler.createFile(values['filename']), values['filetype'])	
			xmlhandler.setFiles(filehandler.getFilenames())
			self.redirect('demo.html')
		#DELETE_ALL
		elif values['action']=='delete_all':
			filehandler.deleteAllFiles()
			xmlhandler.setFiles(filehandler.getFilenames())
			self.redirect('demo.html')
		#DELETE
		elif values['action']=='delete':
			filehandler.deleteFile(values['selected_file'])
			xmlhandler.setFiles(filehandler.getFilenames())
			self.redirect('demo.html')
		#VIEW
		elif values['action']=='view':
			self.redirect('viewfile/'+values['selected_file'])
		#DOWNLOAD
		elif values['action']=='download':
			self.redirect('storedfiles/'+values['selected_file'])
		#Error, print some debugging info
		else:
			print "No/unknown action value returned:",str(values)
			raise IOError
		
		xmlhandler.updateValues(values)		
	
	def redirect(self, location):
		self.send_response(303)
		self.send_header('Location',location)
		self.end_headers()
	
def main():
	try:
	
		server=HTTPServer(('',string.atoi(config.get('general', 'port'))), ReqHandler)
		
		if not scanhandler.supports_brightness_and_contrast() :
			xmlhandler.hideBox('levels')
		xmlhandler.setFiles(filehandler.getFilenames())
		print 'Webserver started. Serving until keyboard interrupt received (ctrl+c)'
		server.serve_forever()
		
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
