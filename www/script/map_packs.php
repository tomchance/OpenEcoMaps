<?php

// Put out a Javascript header and first line
header('Content-Type: text/javascript');
print "var mylayers = new Array();";

// Grab pack identifier
$pack_ident = $_GET['pack'];

// Connect to database
include("../includes/database.inc");

// Grab the pack and print the new default lon/lat
$result = mysql_query("SELECT id, title, lat, lon, zoom FROM packs WHERE identifier = '$pack_ident'");
$pack_data = mysql_fetch_row($result);
$pack_id = $pack_data[0];
print "oem_center_map(" . $pack_data[2] . ", " . $pack_data[3] . ", " . $pack_data[4] . ");";

// Grab the layers info, turn into Javascript
$result = mysql_query("SELECT layers.name FROM layers LEFT JOIN pack_layers ON pack_layers.layer = layers.id WHERE pack_layers.pack = $pack_id");
$i = 0;
while ($layer = mysql_fetch_assoc($result)) {
  $name = $layer['name'];
  $url = $pack_data[1] . "/" . $name . ".kml";
  $url = str_replace(" ", "_", $url);
  $url = strtolower($url);
  print "var mylayer = new Array(); mylayer['name'] = '$name'; mylayer['url'] = 'http://www.openecomaps.co.uk/kml/$url'; mylayers[$i] = mylayer;";
  $i = $i + 1;
}

print "add_pack(mylayers);";
?>