#!/bin/bash
#
# Script for building the website. 
#
# By: Mikko Virkkilä
# License: GPL
# 
if [ -z $1 ]
then
	echo "Usage: $0 [options] targetdirectory"
	echo ""
	echo "Options:"
	echo "--checkout		Check out from svn"
	echo "--noupdate		Don't update version from subversion"
	echo "--nonet			Don't update and don't xinclude remote (will give errors)"
	echo "--nobuild		Don't build html pages"
	exit
fi

NOUPDATE="FALSE"
NOBUILD="FALSE"
CHECKOUT="FALSE"
#if [ `pwd|sed 's/.*\///'` != 'website' ] 
#then 
#	echo "Run script from website directory"
#	exit
#fi

for i in $*
do
	case $i in
	--noupdate)
		NOUPDATE="TRUE"
		;;
	--nobuild)
		NOBUILD="TRUE"
		;;
	--checkout)
		CHECKOUT="TRUE"
		;;
	--nonet)
		NOUPDATE="TRUE"
		PARAMS=$PARAMS' --nonet'
		;;
	*)
		TARGETDIR=$i
		;;
	esac
done


if [ -z $TARGETDIR ]
then 
	if [ $NOBUILD != "TRUE" ]
	then
		echo "You must specify a target dir"
		exit
	fi
fi	


if [ $CHECKOUT = "TRUE" ]
then
	svn checkout svn://svn.berlios.de/websane/website
	chmod a+x website/build.sh
	cd website
fi

if [ $NOUPDATE != "TRUE" ]
then
	svn update
	chmod a+x build.sh
fi

if [ $NOBUILD != "TRUE" ]
then 
	OLD_DIR=`pwd`
	cd $TARGETDIR
	xsltproc $PARAMS --xinclude $OLD_DIR/xslt/builder.xsl $OLD_DIR/xml/site.xml
	cd $OLD_DIR

	
	if [ ! -L $TARGETDIR"/style" ] 
	then
		echo "Creating symlink for the style directory"
		ln -s `pwd`/style $TARGETDIR/style
	fi

fi
