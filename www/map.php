<?php
$map = 1;
$map_max = 1;
$page_title = "the map";
include("includes/header.inc");
?>

<div id="contents" class="solid">
  <div id="text">
    <p>
    Switch to your local map <a href="javascript:switch_to_london();">London</a>, <a href="javascript:switch_to_exeter();">Exeter</a>.
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