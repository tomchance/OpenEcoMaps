old_toggle_sidebar = toggle_sidebar;
toggle_sidebar = function() {
	old_toggle_sidebar();
	size_map_div();
}

function size_map_div() {
	var sidebar = document.getElementById("sidebar");
	var map_div = document.getElementById("map");
	if (sidebar.className == "SidebarVisible") {
		map_div.style.width = document.body.clientWidth - 270;
	} else {
		map_div.style.left = "0px";
		map_div.style.width = document.body.clientWidth - 20;
	}
	if (map)
		map.updateSize();
}

window.attachEvent("onload", size_map_div);