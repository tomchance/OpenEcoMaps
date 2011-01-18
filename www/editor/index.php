<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<head> 
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" /> 
  <link rel="stylesheet" type="text/css" href="../css/site_style.css"> 
<script type="text/javascript" src="swfobject.js"></script>
  <title>OpenEcoMaps :: editor</title> 
</head> 
 
<body> 
 
<div id="edit_header"> 
  <h1>OpenEcoMaps</h1> 
  <p>Free eco-living maps and data from the OpenStreetMap community</p> 
</div> 
 
<div id="edit_menu"> 
  <ul> 
    <li><a href="../index.php">Home</a></li> 
    <li><a href="../map.php">View the map</a></li> 
    <li><a href="../data.php">Use the data</a></li> 
    <li><a href="../contribute.php">Contribute</a></li> 
    <li><a href="../about.php">About OpenEcoMaps</a></li> 
  </ul> 
</div>

<div id="map" style="width:100%; height: 100%; border: 1px solid black">
</div>

<script>
	function getArgs() {
		var args = new Object();
		var query = location.search.substring(1);
		var pairs = query.split("&");
		for(var i = 0; i < pairs.length; i++) {
			var pos = pairs[i].indexOf('=');
			if (pos == -1) continue;
			var argname = pairs[i].substring(0,pos);
			var value = pairs[i].substring(pos+1);
			args[argname] = unescape(value);
		}
		return args;
	}

    var changesaved=true;
  
    window.onbeforeunload=function() {
        if (!changesaved) {
            return 'You have unsaved changes. You need to press the Save button to save them';
        }
    }

    function markChanged(a) { changesaved=a; } /* called from flash */

	var args = getArgs();
	var lat;
	var lon;
	var zoom;
	if (args.lat && args.lon) {
		lat = parseFloat(args.lat);
		lon = parseFloat(args.lon);
	} else {
		lat=51.47395;
		lon=-0.06866;
	}

	if (args.zoom) {
		zoom = parseInt(args.zoom);
	} else {
		zoom = 16;
	}

	var fo = new SWFObject("potlatch2.swf?d="+Math.round(Math.random()*1000), "map", "100%", "100%", "9", "#FFFFFF");
	fo.addVariable("lat",lat);
	fo.addVariable("lon",lon);
	fo.addVariable("zoom",zoom);
	fo.addVariable("api","http://www.openstreetmap.org/api/0.6/");
	fo.addVariable("policy","http://www.openstreetmap.org/api/crossdomain.xml");
	fo.addVariable("connection","XML");
	fo.addVariable("oauth_policy", "http://www.openstreetmap.org/oauth/crossdomain.xml");
	fo.addVariable("oauth_request_url", "http://www.openstreetmap.org/oauth/request_token");
	fo.addVariable("oauth_access_url", "http://www.openstreetmap.org/oauth/access_token");
	fo.addVariable("oauth_auth_url", "http://www.openstreetmap.org/oauth/authorize");
	fo.addVariable("oauth_consumer_key", "k3OLopp5tSrHb2dTkMyV2w");
	fo.addVariable("oauth_consumer_secret", "TpmqRkgYxKFXnkyDWWAIgpdZraUwY8IyrZRWp4Z1Ao");
	fo.addVariable("serverName", "www");
	fo.write("map");


</script>
</div> 
 
</body> 
</html>

