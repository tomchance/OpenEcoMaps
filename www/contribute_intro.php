<?php
$page_title = "introducing OpenStreetMap";
include("includes/header.inc");
?>

<div id="contents">
  <div id="text">
  <h2>Introducing OpenStreetMap</h2>

  <p>To add stuff to the map, you need to:</p>

  <ul>
    <li>Sign up to OpenStreetMap;</li>
    <li>Get out into your local area and note the features you want to add;</li>
    <li>Come back home, load up an editor and add them in.</li>
  </ul>

  <p>OpenStreetMap can be a <em>very</em> confusing beast. At the heart of the project is a database holding all the map data that people work with.</p>

  <p><img src="images/osm-structure.png" alt="OpenStreetMap structure"/></p>

  <p>On the left you have editors that people use to enter data into that database. Some editors work well on mobile phones, others are easy to use but limited in their power, and a few are very hard to learn but extremely powerful.</p>

  <p>On the right, there are all sorts of interesting uses for the data. In the diagram you can see a major online mapping provider, a satnav device and a cycle journey planner all using OpenStreetMap.</p>

  <p>The <strong>data structure</strong> is quite straightforward. For simple features like bus stops, post boxes and cycle racks you have dots (called "nodes"). For linear features like roads, paths, buildings and parks you have lots of dots ("nodes") and they are joined up with lines ("ways"). You can see these below.</p>

  <p><img src="images/osm-data.png" alt="OpenStreetMap data" /></p>

  <p>On the left the nodes and ways are shown as outlines; on the right they are overlaid on top of a fully-drawn map.</p>

  <p>For every feature you add - whether a node or a way - you then add information (called "tags"). Each tag has a key and a value, key=value, for example:</p>

  <ul>
    <li><code>highway=primary</code> <em>(this is a primary highway, i.e. an A-road in the UK)</em></li>
    <li><code>name=Strand</code> <em>(this way is called Strand)</em></li>
    <li><code>maxspeed=30 mph</code> <em>(this way has a maximum speed restriction of 30 miles per hour)</em>)</li>
  </ul>

  <p>Editors let you add and change these nodes and ways; data users take them and draw maps, plan journeys, etc.</p>

  <p>...<br/></p>

  <p><strong>Now you've got the basics sorted, head on to learn <a href="contribute_tutorial.php">how to edit OpenStreetMap</a>.</strong></p>


  </div>
</div>

<?php include("includes/footer.inc"); ?>