<?php
$accordion = 1;
$map = 1;
$map_mini = 1;
$page_title = "home";
include("includes/header.inc");
?>

<div id="contents"> 
  <div id="accordion-container">
    <dl>
	<dt>&rarr; Preview the map</dt>
	<dd><div id="map"></div></dd>
	<dt>&rarr; Use the data</dt>
 	<dd><p>OpenEcoMaps exists to help you put this map on your web site and to use the underlying data yourself, all free of charge.</p><p>You can embed the map on your own web site, zoomed in to your local area and only showing the features you're interested in.</p><p>You can embed the KML files in your own map, if you already have one, to show the features.</p><p>Advanced users can also download the raw data to draw your own maps, analyse it, or do anything else of interest.</p><p>Find out more about <a href="data.php">using the data and maps</a>.</dd> 
	<dt>&rarr; Add to the map</dt>
	<dd><p>You can join the thousands of volunteers who have made this map. All you need to do is go out and survey some features, then come back and add them using the customised OpenEcoMaps editor.</p><p>You can get stuck straight in, if you know what you're doing, by clicking 'Edit here' when zoomed in on <a href="map.php">the map</a>.</p><p>If you're new to OpenStreetMap, we have an introduction to the project, a video tutorial, basic instructions and a practice editor - head over to <a href="contribute.php">learn how to contribute</a>.</dd>
    </dl>
  </div>
</div>

<?php include("includes/footer.inc"); ?>