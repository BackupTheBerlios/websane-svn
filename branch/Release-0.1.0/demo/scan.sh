#!/bin/bash
#
# Copyright (c) 2005 Mikko Virkkilä (mvirkkil@cc.hut.fi)
# 
# This file is part of WebSANE
# 
# WebSANE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# WebSANE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with WebSANE; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

#reset
opts=


#Check if a special binary or path is to be used
if [ -n $PHP_scannerbinary ] 
then 
	PHP_scannerbinary='/usr/bin/scanimage'
fi

#Check if a non default device should be used
if [ $PHP_scandev ]
then 
	opts=$opts+'--device='$PHP_scandev
fi

#Check if a special mode should be used
if [ $PHP_mode ]
then
	opts=$opts' --mode='$PHP_mode
fi

if [ $PHP_brightness ]
then
	opts=$opts' --brightenss='$PHP_brightness
fi

if [ $PHP_contrast ]
then
	opts=$opts' --contrast='$PHP_contrast
fi

#If no dir specified, use current dir
if [ -n $PHP_dir ]
then
	PHP_dir='.'
fi



#Preview mode options
if [[ $PHP_isPreview = 'false' ]]
then
	
opts=$opts\
' --resolution='$PHP_resolution\
' --l='$PHP_leftcoord\
' --t='$PHP_topcoord\
' --x='$PHP_width\
' -y='$PHP_height

file=$PHP_dir$PHP_filename

else 

opts=$opts\
\
' --preview=yes'\
' --resolution=24'\
' --speed=Fast'\
' -l 0'\
' -t 0'\
' -x 230'\
' -y 370'

file=$PHP_dir'/preview.pnm'

fi


echo "$PHP_scannerbinary $opts > $file 2> $PHP_dir/err.log"
