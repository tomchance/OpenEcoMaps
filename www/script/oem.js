var map;

/**
 * Function: initMap
 * Sets up the map, its layers and controls.
 * lat, lon, zoom are the initial map position, provided a permalink has not been used
 */
function initMap(lat, lon, zoom){
  map = new OpenLayers.Map('map',
	  { maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
	    units: 'm',
	    controls: [],
	    projection: new OpenLayers.Projection("EPSG:900913"),
	    displayProjection: new OpenLayers.Projection("EPSG:4326")
	  });

   OpenLayers.ImgPath = "/ol_theme_green/";

  var layerCloudMade = new OpenLayers.Layer.OSM("Default map",
	["http://a.tile.cloudmade.com/8bafab36916b5ce6b4395ede3cb9ddea/27911/256/${z}/${x}/${y}.png",
	"http://b.tile.cloudmade.com/8bafab36916b5ce6b4395ede3cb9ddea/27911/256/${z}/${x}/${y}.png",
	"http://c.tile.cloudmade.com/8bafab36916b5ce6b4395ede3cb9ddea/27911/256/${z}/${x}/${y}.png"],
	{ resolutions: [76.43702827148438, 38.21851413574219,19.109257067871095, 9.554628533935547, 4.777314266967774, 2.3886571, 1.1943286],
	  zoomOffset: 11,
	  numZoomLevels: 7 });
  var layerCycling = new OpenLayers.Layer.OSM("Cycling map",
	["http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
         "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
         "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png"],
	{ attribution: 'Data, imagery and map information provided by <a href="http://www.openstreetmap.org">OpenStreetMap</a> and contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>.',
	  buffer: 0,
	  resolutions: [76.43702827148438, 38.21851413574219,19.109257067871095, 9.554628533935547, 4.777314266967774, 2.3886571, 1.1943286],
	  zoomOffset: 11,
	  numZoomLevels: 7 });
  var layerPublicTransport = new OpenLayers.Layer.OSM("Public transport",
	"http://tile.xn--pnvkarte-m4a.de/tilegen/${z}/${x}/${y}.png",
	{ attribution: 'Data, imagery and map information provided by <a href="http://www.openstreetmap.org">OpenStreetMap</a> and contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>.',
	  buffer: 0,
	  resolutions: [76.43702827148438, 38.21851413574219,19.109257067871095, 9.554628533935547, 4.777314266967774, 2.3886571, 1.1943286],
	  zoomOffset: 11,
	  numZoomLevels: 7 });
  var layerAerial = new OpenLayers.Layer.Bing(
	{ name: "Aerial photography",
	  key: 'AoGQ41xJtaeTYW-5bGSuE7e589v03uKnxXeXmtFEsWMH1UoZMyhBydLItxE7Qua_',
	  type: 'Aerial' });
  map.addLayers([layerCloudMade, layerCycling, layerPublicTransport, layerAerial]);
  
  map.addControl(new OpenLayers.Control.PanZoomBar());
  map.addControl(new OpenLayers.Control.Attribution());
  map.addControl(new OpenLayers.Control.Navigation());
  map.addControl(new OpenLayers.Control.Permalink());
  var layerSwitcherControl = new OpenLayers.Control.LayerSwitcher();
  map.addControl(layerSwitcherControl);
  layerSwitcherControl.maximizeControl();

  if (!map.getCenter()) {
    var lonLat = new OpenLayers.LonLat(lat, lon).transform(map.displayProjection,  map.projection);
    map.setCenter (lonLat, zoom);
  }

  if (map.getCenter()) {
    curLonLat = map.getCenter().transform(map.projection,  map.displayProjection);
    if (curLonLat.lon > -0.51 && curLonLat.lat > 51.20 && curLonLat.lon < 0.35 && curLonLat.lat < 51.80) {
      add_layers_london();
    } else if (curLonLat.lon > -3.667 && curLonLat.lat > 50.626 && curLonLat.lon < -3.3209 && curLonLat.lat < 50.8491) {
      add_layers_exeter();
    }
  }

  return map;
}

/**
 * Function: addKMLLayer
 * Sets up a KML layer with popup classes
 * layername and layerurl are pretty self-explanatory
 */
function addKMLLayer(layername,layerurl){
  var kmllayer = new OpenLayers.Layer.GML(layername, layerurl,
  {
    format: OpenLayers.Format.KML,
    projection: new OpenLayers.Projection("EPSG:4326"),
    visibility: false,
    formatOptions: {
      extractStyles: true,
      extractAttributes: true
    }
  });
  return kmllayer;
}

/**
 * Various functions for popup windows
 */
function onPopupClose(evt) {
//  selectControl.unselect(selectedFeature);
  onFeatureUnselect(selectedFeature);
}
function onFeatureSelect(feature) {
  selectedFeature = feature;
  popup = new OpenLayers.Popup.FramedCloud("chicken", 
    feature.geometry.getBounds().getCenterLonLat(),
    new OpenLayers.Size(100,100),
      "<div><strong>"+feature.attributes.name+"</strong><br/>"+feature.attributes.description+"</div>",
      null, true, onPopupClose);
  feature.popup = popup;
  map.addPopup(popup);
}
function onFeatureUnselect(feature) {
  if (feature.popup) {
    map.removePopup(feature.popup);
    feature.popup.destroy();
    feature.popup = null;
  }
}
/**
 * Various functions for view/edit links on map
 */
function updateLocation() {
  var edit_link = document.getElementById("edit");
  var view_link = document.getElementById("view");
  var all_links = document.getElementsByTagName("a");
  for (var i=0; i < all_links.length; i++) {
    if (all_links[i].innerHTML == "permalink") {
      view_link.href = all_links[i].href;
    }
  }
  var cur_zoom = map.getZoom();
  var cur_lonlat = map.getCenter();
  var cur_lonlat_unproj = cur_lonlat.clone();
  var cur_lonlat_reproj = cur_lonlat_unproj.transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
  var decimals = Math.pow(10, Math.floor(cur_zoom));
  var cur_lat = Math.round(cur_lonlat_reproj.lat * decimals) / decimals;
  var cur_lon = Math.round(cur_lonlat_reproj.lon * decimals) / decimals;
  if (cur_zoom == 6) {
    edit_link.href = "editor/index.php?zoom=17&lon=" + cur_lon + "&lat=" + cur_lat;
    edit_link.className = "edityes";
  } else {
    edit_link.href = "#";
    edit_link.className = "editno";
  }
}

/**
 * Functions to load local-specific layers
 */
function kill_overlays() {
  for (i=map.layers.length-1; i>=0;i--) {
    lyr = map.layers[i];
    if (!lyr.isBaseLayer) {
      map.removeLayer(lyr);
    }
  }
}

function switch_to_london() {
  kill_overlays();
  var lonLat = new OpenLayers.LonLat(-0.1, 51.5).transform(map.displayProjection,  map.projection);
  map.setCenter (lonLat, 1);
  add_layers_london();
}
function add_layers_london() {
  var layerPower = addKMLLayer("Low carbon power",
"http://www.openecomaps.co.uk/kml/london/power.kml");
  var layerWaste = addKMLLayer("Zero waste", "http://www.openecomaps.co.uk/kml/london/waste.kml");
  var layerFood = addKMLLayer("Sustainable food", "http://www.openecomaps.co.uk/kml/london/food.kml");
  var layerTransport = addKMLLayer("Sustainable transport", "http://www.openecomaps.co.uk/kml/london/transport.kml");
  var layerCulture = addKMLLayer("Culture and heritage", "http://www.openecomaps.co.uk/kml/london/culture.kml");
  var layersPOI = [layerPower, layerWaste, layerFood, layerTransport, layerCulture];
  map.addLayers(layersPOI);
  var selectControl = new OpenLayers.Control.SelectFeature(layersPOI, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
  map.addControl(selectControl);
  selectControl.activate();
}

function switch_to_exeter() {
  kill_overlays();
  var lonLat = new OpenLayers.LonLat(-3.51, 50.72).transform(map.displayProjection,  map.projection);
  map.setCenter (lonLat, 1);
  add_layers_exeter();
}
function add_layers_exeter() {
  var layerEPower = addKMLLayer("Low carbon power", "http://www.openecomaps.co.uk/kml/exeter/power.kml");
  var layerEWaste = addKMLLayer("Zero waste", "http://www.openecomaps.co.uk/kml/exeter/waste.kml");
  var layerEFood = addKMLLayer("Sustainable food", "http://www.openecomaps.co.uk/kml/exeter/food.kml");
  var layerETransport = addKMLLayer("Sustainable transport", "http://www.openecomaps.co.uk/kml/exeter/transport.kml");
  var layersEPOI = [layerEPower, layerEWaste, layerETransport, layerEFood];
  map.addLayers(layersEPOI);
  var selectControl = new OpenLayers.Control.SelectFeature(layersEPOI, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
  map.addControl(selectControl);
  selectControl.activate();
}