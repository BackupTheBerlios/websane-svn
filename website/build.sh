#!/bin/bash

if [ `pwd|sed 's/.*\///'` = 'website' ] 
then 
	echo "Create a symlink in the parent directory and rund from there instead"
	exit
fi

if [ -d "website" ]
then
	svn update website
else 
	svn checkout svn://svn.berlios.de/websane/website
	chmod a+x website/build.sh
fi

xsltproc --xinclude website/xslt/builder.xsl website/xml/site.xml

if [ ! -L "style" ] 
then
	echo "Creating symlink for style"
	ln -s website/style `pwd`/style
fi
if [ ! -L "images" ] 
then
	echo "Creating symlink for style"
	ln -s website/images `pwd`/images
fi
if [ ! -L "build.sh" ]
then
	echo "Removing old build.sh"
	rm build.sh
	echo "Symlinkin to new build.sh"
	ln -s website/build.sh ./build.sh
fi

