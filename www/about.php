<?php
$page_title = "about";
include("includes/header.inc");
?>

<div id="contents">
  <div id="text">
  <h2>About OpenEcoMaps</h2>

  <p>OpenEcoMaps provides free eco-living maps and data from <a href="http://www.openstreetmap.org">OpenStreetMap</a>.</p>

  <h3>But why?</h3>

  <p>There are lots of community groups, councils and companies out there mapping allotments, renewable energy generators, cycle routes and more. But they all suffer from two shortcomings:</p>

  <ol>
    <li><strong>Silos and duplication</strong> - by putting their work into different places, different maps, we're storing all of our information in disconnected silos, duplicating effort and not benefiting from each other's work. For example, it's common to find several different people all trying to map food growing spaces in the same part of town. Why not share?</li>
    <li><strong>Tools</strong> - not everybody has the tools to map these things, to put the results onto their web site or provide it to their council in the correct format.</li>
  </ol>

  <p>OpenEcoMaps encourages people to share all their data in the same place - OpenStreetMap - and makes it easier for you to make use of the results.</p>

  <p>You can watch a presentation I gave to <a href="http://www.crystalpalacetransition.org.uk/">Crystal Palace Transition Town</a> to find out more about the motivation behind the project, and why you might want to use it.</p>

  <iframe width="680" height="480" src="//www.youtube.com/embed/Hzyu-o-NADk" frameborder="0" allowfullscreen></iframe>

  <h3>How does it work?</h3>

  <p>OpenEcoMaps takes open data from <a href="http://www.openstreetmap.org">OpenStreetMap</a>, a community that is mapping the whole world and providing all of the information as <a href="http://www.opendefinition.org/okd/">open data</a>. It takes a fresh data extract every hour for each local map, filters this to just show the features of interest, and turns them into layers of icons that can easily be displayed on a map. These layers are provided in a ready-to-use map, and as <a href="https://en.wikipedia.org/wiki/Keyhole_Markup_Language">KML</a> and <a href="https://en.wikipedia.org/wiki/GeoJSON">GeoJSON</a> files so you can use the layers in your own existing maps or other software.</p>

  <p>You can read the documentation on the <a href="http://wiki.openstreetmap.org/wiki/OpenEcoMaps">OpenStreetMap wiki page</a>, including the <a href="http://wiki.openstreetmap.org/wiki/OpenEcoMaps/tags">list of tags</a> we use..</p>

  <p>You can download the code yourself from <a href="https://github.com/tomchance/OpenEcoMaps">this github project</a>.</p>

  <h3>Who does this?</h3>

  <p>OpenEcoMaps was set-up by <a href="http://tom.acrewoods.net">Tom Chance</a> with the help of Shaun McDonald, Andy Allan and Sam Smith. It is kindly hosted by Shaun. Contact <a href="mailto:tom@acrewoods.net">Tom</a> with any enquiries.</p>
  </div>
</div>

<?php include("includes/footer.inc"); ?>
