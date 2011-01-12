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
  map.addLayers([layerCloudMade, layerCycling, layerPublicTransport]);
  
  var layerPower = addKMLLayer("Low carbon power", "../kml/power.kml");
  var layerWaste = addKMLLayer("Zero waste", "../kml/waste.kml");
  var layerFood = addKMLLayer("Sustainable food", "../kml/food.kml");
  var layerTransport = addKMLLayer("Sustainable transport", "../kml/transport.kml");
  var layerCulture = addKMLLayer("Culture and heritage", "../kml/culture.kml");
  var layersPOI = [layerPower, layerWaste, layerFood, layerTransport, layerCulture];
  map.addLayers(layersPOI);
  var selectControl = new OpenLayers.Control.SelectFeature(layersPOI, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
  map.addControl(selectControl);
  selectControl.activate();  
  
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
  for (var i=0; i < document.links.length; i++) {
    if (document.links[i].text == "Permalink") {
      document.links["view"].href = document.links[i].href;
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
    document.links["edit"].href = "editor/index.php?zoom=17&lon=" + cur_lon + "&lat=" + cur_lat;
    document.links["edit"].className = "edityes";
  } else {
    document.links["edit"].href = "#";
    document.links["edit"].className = "editno";
  }
}