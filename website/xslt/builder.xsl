<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
		version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
		xmlns="http://www.w3.org/1999/xhtml">
		
		
		
	<xsl:output method="xml" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes" omit-xml-declaration="yes" />
	<xsl:include href="commonBits.xsl" />
	<xsl:include href="utils.xsl" />

	<xsl:template match="/site">
		Transformation started
		<xsl:for-each select="page">
			Writing page <xsl:value-of select="@name" />
			<xsl:document href="./{@name}" method="xml" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes" omit-xml-declaration="yes">
				<xsl:apply-templates select="news" />
				<xsl:apply-templates select="htmlPage" />
			</xsl:document>
		</xsl:for-each>
		Transformation done
	</xsl:template>
	
	
	<xsl:template match="htmlPage">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<xsl:call-template name="createHTMLHead" />
			<body>
				<xsl:call-template name="createMenu" />
			
				<div class="leftbar">
					
					<xsl:call-template name="createHeader" />
									
					<div class="content">
						<xsl:apply-templates select="*" mode="copy" />
					</div>
					
					<xsl:call-template name="createFooter" />
				</div>
			</body>
		</html>
	</xsl:template>
	
	<xsl:template match="news">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<xsl:call-template name="createHTMLHead" />
			<xsl:call-template name="createMenu" />
			
			<div class="leftbar">
				
				<xsl:call-template name="createHeader" />
								
				<div class="content">
				
					<xsl:for-each select="item">
						<div class="news_title"><xsl:value-of select="title" /></div>
						<div class="news_time"><xsl:value-of select="author" /> - <xsl:value-of select="date" /></div>
						<div class="news_content"><xsl:apply-templates select="doc/*" mode="copy" /></div>
					</xsl:for-each>
				</div>
				
				<xsl:call-template name="createFooter" />
			</div>
		</html>
		
	</xsl:template>
	


	
	

	
	
</xsl:stylesheet>