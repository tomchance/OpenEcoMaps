<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
  <link rel="stylesheet" type="text/css" href="css/oem_style.css">
  <link rel="stylesheet" type="text/css" href="css/site_style.css">
<?php if ($accordion): ?>
  <link rel="stylesheet" type="text/css" href="css/accordion_style.css">
  <script type="text/javascript" src="script/jquery-1.3.2.min.js"></script>
  <script type="text/javascript" src="script/jquery.easyAccordion.js"></script>
  <script type="text/javascript" src="script/utility.js"></script>
<?php endif; ?>
<?php if ($map_mini): ?>
  <script type="text/javascript" src="script/oem_mini.js"></script>
<?php elseif ($map_max): ?>
  <script type="text/javascript" src="script/oem.js"></script>
<?php endif; ?>
<?php if ($map): ?>
  <script type="text/javascript" src="http://www.openlayers.org/dev/OpenLayers.js"></script>
  <!--[if lt IE 7]>
  <link rel="stylesheet" href="/script/ie6-fix.css" type="text/css">
  <script type="text/javascript" src="/script/ie6-fix.js"></script>
  <![endif]-->
  <script type="text/javascript">
    function init() {
  <?php if ($map_max): ?>
      initMap();
      updateLocation();
      map.events.register("moveend", map, updateLocation);
      map.events.register("changelayer", map, updateLocation);
  <?php else: ?>
      initMap(-0.081, 51.5043, 3);
  <?php endif; ?>
    }
  </script>
<?php endif; ?>
  <title>OpenEcoMaps :: <?php echo $page_title; ?></title>
  <!--[if !IE 7]>
  <style type="text/css">
    #wrap {display:table;height:100%}
  </style>
  <![endif]-->
</head>

<body onload='init()'>

<div id="wrap">

<div id="header">
  <h1>OpenEcoMaps</h1>
  <p>Free eco-living maps and data from the OpenStreetMap community</p>
</div>

<div id="menu">
  <ul> 
    <li><a href="index.php">Home</a></li>
    <li><a href="map.php?pack=LDN">View the map</a></li>
    <li><a href="data.php">Use the data</a></li>
    <li><a href="areas.php">Add your area</a></li>
    <li><a href="contribute.php">Contribute</a></li>
    <li><a href="about.php">About OpenEcoMaps</a></li>
  </ul>
</div>

<div id="main">