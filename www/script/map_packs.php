<?php

// Put out a Javascript header and first line
header('Content-Type: text/javascript');
print "var mylayers = new Array();";

// Grab pack identifier
$pack_ident = $_GET['pack'];

// Connect to database
include("../includes/database.inc");

// Grab the pack and layers info, turn into Javascript
$result = mysql_query("SELECT id, title, lat, lon, zoom FROM packs WHERE identifier = '$pack_ident'");
$pack_data = mysql_fetch_row($result);
$pack_id = $pack_data[0];
$result = mysql_query("SELECT layers.kml_filename, layers.name FROM layers LEFT JOIN pack_layers ON pack_layers.layer = layers.id WHERE pack_layers.pack = $pack_id");
$i = 0;
while ($layer = mysql_fetch_assoc($result)) {
  $name = $layer['name'];
  $url = $layer['kml_filename'];
  print "var mylayer = new Array(); mylayer['name'] = '$name'; mylayer['url'] = 'http://www.openecomaps.co.uk/kml/$url'; mylayers[$i] = mylayer;";
  $i = $i + 1;
}

print "add_pack(mylayers);";
?>