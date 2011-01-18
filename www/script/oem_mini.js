var map;

/**
 * Function: initMap
 * Sets up the map, its layers and controls.
 * lat, lon, zoom are the initial map position, provided a permalink has not been used
 */
function initMap(lat, lon, zoom){
  map = new OpenLayers.Map('map',
	  { maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
	    numZoomLevels: 10,
	    maxResolution: 'auto',
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
	{ resolutions: [19.109257067871095, 9.554628533935547, 4.777314266967774, 2.3886571, 1.1943286],
	  zoomOffset: 13,
	  numZoomLevels: 5 });
  map.addLayers([layerCloudMade]);
  
  var layerPower = addKMLLayer("Low carbon power", "http://www.openecomaps.co.uk/kml/london/power.kml");
  var layerWaste = addKMLLayer("Zero waste", "http://www.openecomaps.co.uk/kml/london/waste.kml");
  var layerFood = addKMLLayer("Sustainable food", "http://www.openecomaps.co.uk/kml/london/food.kml");
  var layerTransport = addKMLLayer("Sustainable transport", "http://www.openecomaps.co.uk/kml/london/transport.kml");
  var layerCulture = addKMLLayer("Culture and heritage", "http://www.openecomaps.co.uk/kml/london/culture.kml");
  var layersPOI = [layerPower, layerWaste, layerFood, layerTransport, layerCulture];
  map.addLayers(layersPOI);
  var selectControl = new OpenLayers.Control.SelectFeature(layersPOI, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
  map.addControl(selectControl);
  selectControl.activate();  
  
  map.addControl(new OpenLayers.Control.PanZoom());
  map.addControl(new OpenLayers.Control.Navigation());

  var lonLat = new OpenLayers.LonLat(lat, lon).transform(map.displayProjection,  map.projection);
  map.setCenter (lonLat, zoom);

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
    visibility: true,
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
