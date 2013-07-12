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

    <p><code>&lt;iframe  height="500px" width="100%" src="http://www.openecomaps.co.uk/map_embed.php"&gt;<br/>&lt;p&gt;Your browser does not support iframes.&lt;/p&gt;<br/>&lt;/iframe&gt;</code></p>

    <p>To centre the map on your area of interest, with the layers you want activated, navigate to your preferred default view on the <a href="map_embed.php">embeddable map</a> and copy the "Permalink" URL and paste it to replace the URL in the iframe.</p>

    <h3>Using KML and GeoJSON files</h3>

    <p>Alternatively, you can use the KML and/or GeoJSON files for each layer to embed anywhere you like. You can find documentation for adding KML files to an existing Google map <a href="https://developers.google.com/maps/documentation/javascript/layers#KMLLayers">here</a>, and for adding either KML or GeoJSON to a map using the much nicer Leaflet map library <a href="http://leafletjs.com/examples/geojson.html">here</a>.</p> 

    <?php
    // Connect to database
    include("includes/database.inc");

    // Grab the layers info for each pack and print the links
    $pack_result = mysql_query("SELECT id, title FROM packs ORDER BY title ASC");
    while ($pack = mysql_fetch_assoc($pack_result)) {
      print "<h3>" . $pack['title'] . "</h3>\n<ul>";
      // Layers
      $layer_result = mysql_query("SELECT layers.name FROM layers LEFT JOIN pack_layers ON pack_layers.layer = layers.id WHERE pack_layers.pack = " . $pack['id']);
      while ($layer = mysql_fetch_assoc($layer_result)) {
        $name = $layer['name'];
        $url = $pack['title'] . "/" . $name;
        $url = str_replace(" ", "_", $url);
        $url = strtolower($url);
        print '<li>' . $name . ': <a href="/kml/' . $url . '.kml">KML</a>, <a href="/json/' . $url . '.json">GeoJSON</a></li>';
      }
      print "</ul>";
    }
    ?>

    <h2>Getting the raw data</h2> 

    <p>You can download the raw data we are using direct from the OpenStreetMap servers using the <a href="https://wiki.openstreetmap.org/wiki/Overpass_API">Overpass API</a>. Read that wiki page to understand how to use it, and the nifty <a href="http://overpass-turbo.eu/">Overpass turbo</a> tool to experiment with the queries you use to download the data. To give you a head start, here is a query that will download all the power generators in the Greater London area:</p> 

    <p><code>(<br/>
  node<br/>
    ["power"="generator"]<br/>
    (51.20,-0.51,51.80,0.35);<br/>
  way<br/>
    ["power"="generator"]<br/>
    (51.20,-0.51,51.80,0.35);<br/>
  rel<br/>
    ["power"="generator"]<br/>
    (51.20,-0.51,51.80,0.35);<br/>
);<br/>
(._;>;);<br/>
out;</code></p>

    <p>You can see the results of this on a web map <a href="http://www.overpass-api.de/api/convert?data=%28%0D%0A++node%0D%0A++++%5B%22power%22%3D%22generator%22%5D%0D%0A++++%2851.20%2C-0.51%2C51.80%2C0.35%29%3B%0D%0A++way%0D%0A++++%5B%22power%22%3D%22generator%22%5D%0D%0A++++%2851.20%2C-0.51%2C51.80%2C0.35%29%3B%0D%0A++rel%0D%0A++++%5B%22power%22%3D%22generator%22%5D%0D%0A++++%2851.20%2C-0.51%2C51.80%2C0.35%29%3B%0D%0A%29%3B%0D%0A%28._%3B%3E%3B%29%3B%0D%0Aout%3B&target=ol_fixed">here</a>.</p>

    <p>Once you have the data - provided in the <a href="http://wiki.openstreetmap.org/wiki/Data_Primitives">OpenStreetMap XML format</a> - you can play with that or convert it into other formats.</p> 

    <p>You can also download complete dumps of OpenStreetMap data as other formats including Shapefiles. See these pages for <a href="http://wiki.openstreetmap.org/wiki/Shapefiles">shapefiles</a>, <a href="http://wiki.openstreetmap.org/wiki/SVG">SVG graphics</a> and <a href="http://wiki.openstreetmap.org/wiki/Convert">other formats</a>.</p> 
  </div>
</div>

<?php include("includes/footer.inc"); ?>
