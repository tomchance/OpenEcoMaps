<?xml version="1.0" encoding="UTF-8"?>
 
<!DOCTYPE xsl:stylesheet [
<!ENTITY tab '<xsl:text xmlns:xsl="http://www.w3.org/1999/XSL/Transform">&#9;</xsl:text>'>
<!ENTITY cr '<xsl:text xmlns:xsl="http://www.w3.org/1999/XSL/Transform">&#13;</xsl:text>'>
<!ENTITY quot '<xsl:text xmlns:xsl="http://www.w3.org/1999/XSL/Transform">&#34;</xsl:text>'>
]>
 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 
<!-- XSLT to extract amenities from OSM data.
Takes seven parameters and returns a tab-delimited text file suitable
for use with OpenLayers.
 
key: The osm key to match, e.g. 'amenity'
value: The value of the key for the items that are to be extracted, e.g. 'library'
icon: The filename of the icon to use for this point
width,height: The width and height of the icon
offsetx,offsety: The icon offset
 
The first two parameters are used to extract objects from the OSM XML.
The last five parameters are written verbatim to the columns in the
output text file.
 
Objects which are nodes are returned as the single lat/lon pair
for each node.
Objects which are areas are returned as a single lat/lon pair for
the centroid of the area.  The centroid is a cheap average, which is
adequate for this purpose.
 
The text in the popup box for each icon is simply the name=* tag for
the object, and a line of text which reads 'node' or 'area' depending
on how the object's lat/lon was extracted.
-->
 
<xsl:output method="text"/>
 
<xsl:template match="osm">lat&tab;lon&tab;amenity&tab;shop&tab;name&tab;description&tab;website&tab;wikipedia&tab;phone&tab;opening_hours&tab;flickr&tab;operator&tab;cuisine&tab;meat&tab;fish&tab;vegetables
<xsl:apply-templates select="node"/>
<xsl:apply-templates select="way"/>
</xsl:template>
 
<xsl:template match="node">
<xsl:for-each select="tag">
<xsl:if test='@k="amenity" or @k="shop"'>
<xsl:value-of select='../@lat'/>&tab;
<xsl:value-of select='../@lon'/>&tab;
<xsl:value-of select='../tag[@k="amenity"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="shop"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="name"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="description"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="website"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="wikipedia"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="phone"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="opening_hours"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="flickr"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="operator"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="cuisine"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="meat"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="fish"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="vegetables"]/@v'/>&cr;
</xsl:if>
</xsl:for-each>
</xsl:template>
 
<xsl:template match="way">
<xsl:variable name="noderefs" select="nd[not(@ref=preceding-sibling::nd/@ref)]"/>
<xsl:variable name="nodes" select="../node[@id=$noderefs/@ref]"/>
<xsl:for-each select="tag">
<xsl:if test='@k="amenity" or @k="shop"'>
<xsl:value-of select="sum($nodes/@lat) div count($nodes)"/>&tab;
<xsl:value-of select="sum($nodes/@lon) div count($nodes)"/>&tab;
<xsl:value-of select='../tag[@k="amenity"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="name"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="shop"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="description"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="website"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="wikipedia"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="phone"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="opening_hours"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="flickr"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="operator"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="cuisine"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="meat"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="fish"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="vegetables"]/@v'/>&cr;
</xsl:if>
</xsl:for-each>
</xsl:template>
 
</xsl:stylesheet>
