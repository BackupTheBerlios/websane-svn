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
import sane
import ConfigParser
from time import time


class ScanHandler:
	SANE_CAP_SOFT_SELECT=1
	SANE_CAP_HARD_SELECT=2
	SANE_CAP_SOFT_DETECT=4
	SANE_CAP_EMULATED=8
	SANE_CAP_AUTOMATIC=16
	SANE_CAP_INACTIVE=32
	SANE_CAP_ADVANCED=64
	
	scanner=None
	scannerdev=None
	rotation=0

	#These are actually how to convert the websane representation of the 
	#width of the image in to mm. I haven't implemented reading the
	#bounds yet.
	magicnum=65536.0
	max_width=14149222.0/magicnum #The 14149222 is the width of the page as reported by python sane.
	max_height=19475988.0/magicnum #height is the height of the page in mm.


	config = ConfigParser.ConfigParser()
	
	#This is a constant and shouldn't be modified
	mmperinch=25.4
	
	#Updates the preview file.
	def update_preview(self, previewfile):
		self.scanner.quality_cal=False
		self.scanner.resolution=self.previewres
		self.scanner.preview=True
		self.scan_and_save(previewfile, 'PNG')

	#Scans a file with the assigned settings and saves it.
	def scan_and_save(self, file, imgtype):
		t=time()				
		self.scanner.start()
		print 'Starting the scanner with the selected options took ',time()-t,'seconds'
		
		t=time()
		im=self.scanner.snap()
		print 'Scanning image took ',time()-t,'seconds'
		
		t=time()
		im=im.rotate(self.rotation)
		print 'Rotating image took ',time()-t,'seconds'
		
		t=time()
		im.save(file, imgtype)
		print 'Converting and saving image took ',time()-t,'seconds\n'
	

	def reset_settings(self):
		self.rotate=0
		t=time()
		self.scanner=sane.open(self.scannerdev)
		print 'Opening the selected device took ', time()-t,'seconds'

	def write_info(self,towriteto):
		towriteto.write( '\n\nSANE version:\n'+str(sane.init()))
		devs = sane.get_devices()
		towriteto.write( '\n\nAvailable devices:\n'+str(devs))
		scanner = sane.open(devs[string.atoi(self.config.get('general','devicenumber'))][0])
		towriteto.write( '\n\nParameters of specified device:\n'+str(scanner.get_parameters()) )
		towriteto.write( '\n\nOptlist:\n')
		towriteto.write( str(scanner.optlist) )
		opts=scanner.get_options()
		towriteto.write( '\n\nActive options:\n')
		for x in opts:
			if self.option_is_active(x[1]):
				towriteto.write( str(x)+'\n' )
		towriteto.write( '\n\nInactive options:\n')
		for x in opts:
			if not self.option_is_active(x[1]):
				towriteto.write( str(x)+'\n' )

	def option_is_active(self, opt):
		opts=self.scanner.get_options()
		for x in opts:
			if x[1] == opt: 
				if (x[7]&self.SANE_CAP_INACTIVE) == self.SANE_CAP_INACTIVE:
					return False
				else:
					return True
		print "Warning, option no found:",opt
		return False

	#Translate the pixel locations in the preview to realworld coordinates (in to mm)
	def set_scan_bounds_from_preview(self, x_px, y_px, width_px, height_px, rotation=0, previewres=None):
		if previewres != None:
			self.previewres=string.atof(previewres)
		top_x=string.atof(x_px) * self.mmperinch / self.previewres 
		top_y=string.atof(y_px) * self.mmperinch / self.previewres
		bottom_x=top_x + string.atoi(width_px) * self.mmperinch / self.previewres
		bottom_y=top_y + string.atoi(height_px) * self.mmperinch / self.previewres
		self.__rotate_coords(top_x,top_y,bottom_x,bottom_y,string.atoi(rotation))
	
	
	def __rotate_coords(self,top_x,top_y,bottom_x,bottom_y,rotation):
		self.rotation=rotation
		if rotation==90:
			self.scanner.tl_y=top_x
			self.scanner.br_x=self.max_width-top_y
			self.scanner.br_y=bottom_x
			self.scanner.tl_x=self.max_width-bottom_y
		elif rotation==180:
			self.scanner.br_x=self.max_width-top_x
			self.scanner.br_y=self.max_height-top_y
			self.scanner.tl_x=self.max_width-bottom_x
			self.scanner.tl_y=self.max_height-bottom_y
		elif rotation==270:
			self.scanner.br_y=self.max_height-top_x
			self.scanner.tl_x=top_y
			self.scanner.tl_y=self.max_height-bottom_x
			self.scanner.br_x=bottom_y
		else: #rotation==0
			self.scanner.tl_x=top_x
			self.scanner.tl_y=top_y
			self.scanner.br_x=bottom_x
			self.scanner.br_y=bottom_y
		
		print "X1:",self.scanner.tl_x
		print "Y1:",self.scanner.tl_y
		print "X2:",self.scanner.br_x
		print "Y2:",self.scanner.br_y
	
	def supports_brightness_and_contrast(self):
		if self.option_is_active('brightness') and self.option_is_active('contrast'):
			print "Brightness and contrast are supported"
			return True
		else:
			print "Brightness and contrast are not supported"
			return False

	def set_brightness_and_contrast(self, brightness,contrast):
		if (self.supports_brightness_and_contrast()):
			self.scanner.brightness=brightness
			self.scanner.contrast=contrast
		else:
			print "Brightness/contrast not supported by scanner"
			
	def set_preview_rotation(self, rotation):
		self.rotation=rotation
		
	def set_resolution(self, resolution):
		self.scanner.resolution=string.atof(resolution)
	
	''' imagemode:
			BW - for black and white (lineart) scans
			GRAY - for grayscale scans
			COLOR - for color scans
			any other will use COLOR
	'''
	def set_mode(self, imagemode):
		if imagemode == None:
			self.scanner.mode='Color'
		elif imagemode == 'BW':
			self.scanner.mode='Lineart'
		elif imagemode == 'GRAY':
			self.scanner.mode='Gray'
		else:
			self.scanner.mode='Color'	
	
	def __init__(self):
		
		self.config.read("scanner.cfg")
		self.previewres=string.atof(self.config.get('general','previewres'))
		print "Reading config file done"

		t=time()
		print 'Initializing scanner ', sane.init(),
		print time()-t,'seconds'

		t=time()
		devs=sane.get_devices()
		print 'Fetching available devices took ',time()-t,'seconds'
			
		self.scannerdev=devs[string.atoi(self.config.get('general','devicenumber'))][0]
			
		self.reset_settings()
