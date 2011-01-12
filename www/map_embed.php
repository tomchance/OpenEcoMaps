<html xmlns="http://www.w3.org/1999/xhtml"> 
 
  <head>
    <link rel="stylesheet" type="text/css" href="css/oem_style.css">
    <script type="text/javascript" src="http://www.openlayers.org/api/OpenLayers.js"></script> 
    <script type="text/javascript" src="script/oem.js"></script> 
	<!--[if lt IE 7]>
	<link rel="stylesheet" href="/script/ie6-fix.css" type="text/css">
	<script type="text/javascript" src="/script/ie6-fix.js"></script>
	<![endif]--> 
    <script type="text/javascript"> 
      function init() {
        initMap(-0.1, 51.5, 1);
	updateLocation();
	map.events.register("moveend", map, updateLocation);
      }
    </script>
  </head> 
 
  <body onload="init()">
 
    <?php if (!$_GET['zoom']): ?>
    <div id="bigfatviewlink"><a href="map_embed.php" id="view" title="Link to this view">Copy this once you have zoomed to the right place and turned on the layers you want.</a></div>
    <div style="display: none;"><a href="" id="edit">Edit.</a></div>
    <?php endif; ?>

    <div id="map"></div>
 
  </body> 
 
</html>  
