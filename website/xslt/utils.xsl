<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
		version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
		xmlns="http://www.w3.org/1999/xhtml">
		
	<xsl:template match="*" priority="-1" mode="copy">
		<xsl:element name="{name()}">
		<xsl:copy-of select="@*"/>
		<xsl:apply-templates mode="copy"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="text()" mode="copy">
		<xsl:value-of select="."/>
		<!--<xsl:value-of select="normalize-space(.)"/>-->
	</xsl:template>
	
	
	<xsl:template name="txttolink">
		<xsl:param name="txt" />
		<xsl:choose>
			<xsl:when test="contains($txt,'http:')">
				<xsl:value-of select="substring-before($txt,'http:')" />
				<xsl:variable name="link">
					<xsl:value-of select="substring-before(substring-after($txt,'http:'), ' ')" />
				</xsl:variable>
				<a>
					<xsl:attribute name="href">http:<xsl:value-of select="$link" /></xsl:attribute>
					http:<xsl:value-of select="$link" />
				</a>
				<xsl:call-template name="txttolink" >
					<xsl:with-param name="txt" select="substring-after($txt,$link)" />
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$txt" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	
	
	
		
</xsl:stylesheet>