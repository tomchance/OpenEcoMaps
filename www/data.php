<?php
$page_title = "use the data";
include("includes/header.inc");
?>

<div id="contents" class="solid">
  <div id="text">
    <h2>Using the map on your web site</h2> 

    <p>There are two ways to use these maps on your web site.</p>

    <h3>Embedding the map</h3>

    <p>The first and most simple way is to simply embed the map in an iframe. If you can add HTML content, you can add this:</p> 

    <p><code>&lt;iframe  height="500px" width="100%" src="http://www.openecomaps.org/map_embed.php"&gt;<br/>&lt;p&gt;Your browser does not support iframes.&lt;/p&gt;<br/>&lt;/iframe&gt;</code></p>

    <p>To centre the map on your area of interest, with the layers you want activated, navigate to your preferred default view on the <a href="map_embed.php">embeddable map</a> and copy the "Permalink" URL and paste it to replace the URL in the iframe.</p>

    <h3>Using KML files</h3>

    <p>Alternatively, you can use the KML feeds for each layer to embed anywhere you like. They are:</p> 

    <ul> 
      <li>Power - <a href="http://www.openecomaps.org/kml/london/power.kml">KML</a></li> 
      <li>Food - <a href="http://www.openecomaps.org/kml/london/food.kml">KML</a></li> 
      <li>Waste - <a href="http://www.openecomaps.org/kml/london/waste.kml">KML</a></li> 
      <li>Transport - <a href="http://www.openecomaps.org/kml/london/transport.kml">KML</a></li> 
      <li>Culture - <a href="http://www.openecomaps.org/kml/london/culture.kml">KML</a></li>
    </ul> 

    <h2>Getting the raw data</h2> 

    <p>You can download the raw data we are using direct from the OpenStreetMap servers using the <a href="http://wiki.openstreetmap.org/wiki/Xapi">eXtended API</a>. Read that wiki page to understand how to use it. To give you a head start, here is a query that will download all the power generators in the Greater London area or the UK:</p> 

    <p><code>http://xapi.openstreetmap.org/api/0.6/*[power=generator][bbox=-0.51,51.20,0.35,51.80]</code> <em>(Greater London)</em><br/> 
	<code>http://xapi.openstreetmap.org/api/0.6/*[power=generator][bbox=-6.5,49.68,2.67,61.31]</code> <em>(UK)</em></p> 

    <p>Once you have the data - provided in the <a href="http://wiki.openstreetmap.org/wiki/Data_Primitives">OpenStreetMap XML format</a> - you can play with that or convert it into other formats.</p> 

    <p>You can also download complete dumps of OpenStreetMap data as other formats including Shapefiles. See these pages for <a href="http://wiki.openstreetmap.org/wiki/Shapefiles">shapefiles</a>, <a href="http://wiki.openstreetmap.org/wiki/SVG">SVG graphics</a> and <a href="http://wiki.openstreetmap.org/wiki/Convert">other formats</a>.</p> 
  </div>
</div>

<?php include("includes/footer.inc"); ?>
