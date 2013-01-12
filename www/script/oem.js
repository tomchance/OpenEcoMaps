var map;

/**
 * Function: initMap
 * Sets up the map, its layers and controls.
 * lat, lon, zoom are the initial map position, provided a permalink has not been used
 */
function initMap(){
  map = new OpenLayers.Map('map',
	  { maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
	    units: 'm',
	    controls: [],
	    projection: new OpenLayers.Projection("EPSG:900913"),
	    displayProjection: new OpenLayers.Projection("EPSG:4326")
	  });

   OpenLayers.ImgPath = "/ol_theme_green/";

  var layerMapBox = new OpenLayers.Layer.OSM("Default map",
	["http://a.tiles.mapbox.com/v3/tomchance.map-hr1423ep/${z}/${x}/${y}.png",
    "http://b.tiles.mapbox.com/v3/tomchance.map-hr1423ep/${z}/${x}/${y}.png",
    "http://c.tiles.mapbox.com/v3/tomchance.map-hr1423ep/${z}/${x}/${y}.png",
    "http://d.tiles.mapbox.com/v3/tomchance.map-hr1423ep/${z}/${x}/${y}.png"],
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
	["http://a.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png",
	"http://b.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png",
	"http://c.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png"],
	{ attribution: 'Data, imagery and map information provided by <a href="http://www.openstreetmap.org">OpenStreetMap</a> and contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>.',
	  buffer: 0,
	  resolutions: [76.43702827148438, 38.21851413574219,19.109257067871095, 9.554628533935547, 4.777314266967774, 2.3886571, 1.1943286],
	  zoomOffset: 11,
	  numZoomLevels: 7 });
  var layerAerial = new OpenLayers.Layer.Bing(
	{ name: "Aerial photography",
	  key: 'AoGQ41xJtaeTYW-5bGSuE7e589v03uKnxXeXmtFEsWMH1UoZMyhBydLItxE7Qua_',
	  type: 'Aerial' });
  map.addLayers([layerMapBox, layerCycling, layerPublicTransport, layerAerial]);
  
  map.addControl(new OpenLayers.Control.PanZoomBar());
  map.addControl(new OpenLayers.Control.Attribution());
  map.addControl(new OpenLayers.Control.Navigation());
  map.addControl(new OpenLayers.Control.Permalink());
  var layerSwitcherControl = new OpenLayers.Control.LayerSwitcher();
  map.addControl(layerSwitcherControl);
  layerSwitcherControl.maximizeControl();

  var pack = gup('pack');
  script = document.createElement('script');
  script.src = '/script/map_packs.php?pack=' + pack;
  document.getElementsByTagName( 'head' )[0].appendChild(script);

  return map;
}

/*
 * Center the map on pack defaults if arguments haven't been passed in URL
 */
function oem_center_map(lat, lon, zoom) {  
  if (!map.getCenter()) {
    var lonLat = new OpenLayers.LonLat(lon, lat).transform(map.displayProjection,  map.projection);
    map.setCenter (lonLat, zoom);
  }
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
    visibility: false,
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
/**
 * Various functions for view/edit links on map
 */
function updateLocation() {
  var edit_link = document.getElementById("edit");
  var view_link = document.getElementById("view");
  var all_links = document.getElementsByTagName("a");
  for (var i=0; i < all_links.length; i++) {
    if (all_links[i].innerHTML == "Permalink") {
      view_link.href = all_links[i].href;
    }
  }
  var cur_zoom = map.getZoom();
  var cur_lonlat = map.getCenter();
  var cur_lonlat_unproj = cur_lonlat.clone();
  var cur_lonlat_reproj = cur_lonlat_unproj.transform(map.projection,  map.displayProjection);
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
 * Function to load pack of local-specific layers
 */
function add_pack(layerdef) {
  var poiLayers = new Array();
  for (var i=0; i < layerdef.length; i++) {
    poiLayers[i] = addKMLLayer(layerdef[i].name, layerdef[i].url);
  }
  map.addLayers(poiLayers);
  var selectControl = new OpenLayers.Control.SelectFeature(poiLayers, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
  map.addControl(selectControl);
  selectControl.activate();
}

/*
 * Amazing, silly function just to ger URL arguments
 */
function gup( name )
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}
