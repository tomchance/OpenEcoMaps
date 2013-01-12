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
  
  var layerPower = addKMLLayer("Low carbon power", "http://www.openecomaps.co.uk/kml/one_planet_london/low_carbon_power.kml");
  var layerFood = addKMLLayer("Food", "http://www.openecomaps.co.uk/kml/one_planet_london/food.kml");
  var layersPOI = [layerPower, layerFood];
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
  var kmllayer = new OpenLayers.Layer.Vector(layername, {
    strategies: [new OpenLayers.Strategy.Fixed()],
    projection: new OpenLayers.Projection("EPSG:4326"),
    visibility: true,
    protocol: new OpenLayers.Protocol.HTTP({
      url: layerurl,
      format: new OpenLayers.Format.KML({
        extractStyles: true, 
        extractAttributes: true,
      })
    })
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
      "<div><h3>"+feature.attributes.name+"</h3>"+feature.attributes.description+"</div>",
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
