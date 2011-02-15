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
 
<xsl:template match="osm">lat&tab;lon&tab;name&tab;description&tab;website&tab;wikipedia&tab;flickr&tab;amenity&tab;operator&tab;recycling:aluminium&tab;recycling:batteries&tab;recycling:books&tab;recycling:cans&tab;recycling:cardboard&tab;recycling:cartons&tab;recycling:cds&tab;recycling:chipboard&tab;recycling:christmas_trees&tab;recycling:clothes&tab;recycling:cooking_oil&tab;recycling:cork&tab;recycling:electrical_items&tab;recycling:engine_oil&tab;recycling:excrement&tab;recycling:fluorescent_tubes&tab;recycling:foil&tab;recycling:glass&tab;recycling:glass_bottles&tab;recycling:green_waste&tab;recycling:garden_waste&tab;recycling:hardcore&tab;recycling:low_energy_bulbs&tab;recycling:magazines&tab;recycling:mobile_phones&tab;recycling:newspaper&tab;recycling:paint&tab;recycling:paper&tab;recycling:paper_packaging&tab;recycling:plasterboard&tab;recycling:plastic_bags&tab;recycling:plastic_bottles&tab;recycling:plastic_packaging&tab;recycling:polyester&tab;recycling:printer_cartridges&tab;recycling:scrap_metal&tab;recycling:sheet_metal&tab;recycling:small_appliances&tab;recycling:tyres&tab;recycling:tv_monitor&tab;recycling:waste&tab;recycling:wood
<xsl:apply-templates select="node"/>
<xsl:apply-templates select="way"/>
</xsl:template>
 
<xsl:template match="node">
<xsl:for-each select="tag">
<xsl:if test='@k="amenity" @k="landuse"'>
<xsl:value-of select='../@lat'/>&tab;
<xsl:value-of select='../@lon'/>&tab;
<xsl:value-of select='../tag[@k="name"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="description"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="website"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="wikipedia"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="flickr"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="amenity"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="operator"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:aluminium"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:batteries"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:books"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cans"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cardboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cartons"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cds"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:chipboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:christmas_trees"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:clothes"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cooking_oil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cork"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:electrical_items"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:engine_oil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:excrement"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:fluorescent_tubes"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:foil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:glass"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:glass_bottles"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:green_waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:garden_waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:hardcore"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:low_energy_bulbs"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:magazines"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:mobile_phones"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:newspaper"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paint"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paper"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paper_packaging"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plasterboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_bags"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_bottles"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_packaging"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:polyester"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:printer_cartridges"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:scrap_metal"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:sheet_metal"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:small_appliances"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:tyres"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:tv_monitor"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:wood"]/@v'/>&cr;
</xsl:if>
</xsl:for-each>
</xsl:template>
 
<xsl:template match="way">
<xsl:variable name="noderefs" select="nd[not(@ref=preceding-sibling::nd/@ref)]"/>
<xsl:variable name="nodes" select="../node[@id=$noderefs/@ref]"/>
<xsl:for-each select="tag">
<xsl:if test='@k="amenity" @k="landuse"'>
<xsl:value-of select="sum($nodes/@lat) div count($nodes)"/>&tab;
<xsl:value-of select="sum($nodes/@lon) div count($nodes)"/>&tab;
<xsl:value-of select='../tag[@k="name"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="description"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="website"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="wikipedia"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="flickr"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="amenity"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="operator"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:aluminium"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:batteries"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:books"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cans"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cardboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cartons"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cds"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:chipboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:christmas_trees"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:clothes"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cooking_oil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:cork"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:electrical_items"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:engine_oil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:excrement"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:fluorescent_tubes"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:foil"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:glass"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:glass_bottles"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:green_waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:garden_waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:hardcore"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:low_energy_bulbs"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:magazines"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:mobile_phones"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:newspaper"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paint"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paper"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:paper_packaging"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plasterboard"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_bags"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_bottles"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:plastic_packaging"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:polyester"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:printer_cartridges"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:scrap_metal"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:sheet_metal"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:small_appliances"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:tyres"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:tv_monitor"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:waste"]/@v'/>&tab;
<xsl:value-of select='../tag[@k="recycling:wood"]/@v'/>&cr;
</xsl:if>
</xsl:for-each>
</xsl:template>
 
</xsl:stylesheet>
