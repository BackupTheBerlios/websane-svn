<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
		version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
		xmlns="http://www.w3.org/1999/xhtml">
	
		
	
		
	<xsl:template name="createHTMLHead">
		<head>
			<title>WebSANE
				<xsl:if test="@title">
					- <xsl:value-of select="@title" />
				</xsl:if>
			</title>
			<link rel="stylesheet" type="text/css" href="style/css/default.css"> </link>
			<link rel="stylesheet" type="text/css" href="style/css/head.css"> </link>
			<link rel="stylesheet" type="text/css" href="style/css/leftbar.css"> </link>
			<link rel="stylesheet" type="text/css" href="style/css/content.css"> </link>
			<link rel="stylesheet" type="text/css" href="style/css/tail.css"> </link>
			<link rel="stylesheet" type="text/css" href="style/css/box.css"> </link>
		</head>
	</xsl:template>
	
	
	
	
	
	<xsl:template name="createHeader">
		<div class="head">
				<h1>WebSANE</h1>
				<h2>Web frontend for SANE</h2>
		</div>
	</xsl:template>
	
	
		
	
	
	
	<xsl:template name="createMenu">
		<div class="rightbar">
			<ul>
				<xsl:for-each select="/site/page" >
					<xsl:if test="@inmenu='yes'">
						<li>
							<a>
								<xsl:attribute name="href"><xsl:value-of select="@name" /></xsl:attribute>
								<xsl:value-of select="@menutitle" />
							</a>
						</li>
					</xsl:if>
				</xsl:for-each>
			</ul>
		</div>
	</xsl:template>
	
	
	
	<xsl:template name="createFooter">
		<div class="tail">
			<a href="http://validator.w3.org/check?uri=referer"><img src="style/images/xhtml.png" title="Valid XHTML 1.0 Strict" alt="Valid XHTML 1.0 Strict" height="15" width="80" /></a>
			<a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="style/images/css.png" title="Valid CSS" alt="Valid CSS" height="15" width="80" /></a>
			<a href="http://www.getfirefox.com"><img src="style/images/ff.png" title="WebSANE recommends Firefox" alt="Firefox preferred" height="15" width="80" /></a>
			<br />Copyright 2005 Mikko Virkkilä<br />
			<a href="http://developer.berlios.de/projects/websane/">
				<img src="http://developer.berlios.de/bslogo.php?group_id=3028&amp;type=1" title="WebSANE project page on BerliOS" alt="WebSANE project page on BerliOS" />
			</a>
		</div>
	</xsl:template>
		
		
</xsl:stylesheet>