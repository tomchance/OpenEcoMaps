<?php
$map = 1;
$map_max = 1;
$page_title = "the map";
include("includes/header.inc");
include("includes/database.inc");
?>

<div id="contents" class="solid">
  <div id="text">
    <p>
    Switch to your local map: <?php
// Grab the pack and layers info, turn into Javascript
$result = mysql_query("SELECT identifier, title, lon, lat, zoom FROM packs");
while ($pack = mysql_fetch_assoc($result)) {
  print "<a href=\"map.php?pack=" . $pack['identifier'] . "&zoom=" . $pack['zoom'] . "&lon=" . $pack['lon'] . "&lat=" . $pack['lat'] . "\">" . $pack['title'] . "</a> ";
}
?>
    </p>
  <div id="maplinks">
    <ul>
      <li><a href="map.php" class="" id="view" title="Link to this view">Link here</a></li>
      <li><a href="#" class="" id="edit" title="Edit the map">Edit here</a></li>
    </ul>
  </div>
  <div id="map"></div>
  </div>
</div>

<?php include("includes/footer.inc"); ?>