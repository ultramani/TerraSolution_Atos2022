//map
const map = L.map('map').setView([40, -3], 7);
map.zoomControl.setPosition('topright');
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//--------------------------------------------------------------------------------------------------------------------------------------------
//longitude event

var input = document.getElementById("longitude");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("coordsBtn").click();
  }
});

//--------------------------------------------------------------------------------------------------------------------------------------------
//geoman
map.pm.addControls({  
    position: 'topright',  
    drawMarker: false,
    drawPolyline: false,
    drawCircle: false,
    drawRectangle: false,
    // drawPolygon: false,
    drawCircleMarker: false,
    editMode: false,
    dragMode: false,
    cutPolygon: false,
    removalMode: false,
    rotateMode: false,
}); 

map.pm.Toolbar.setButtonDisabled('drawPolygon', true);

//Limit side of polygon
map.on('pm:drawstart', function(e) {
    if(window.polygon !== undefined){
        map.removeLayer(window.polygon);
    }
    var nVertex = 0;
    e.workingLayer.on('pm:vertexadded', function(e) {
        nVertex += 1;
        if(nVertex >10){
            map.pm.Draw.Polygon._removeLastVertex();
            nVertex -= 1;
            jQuery(function($) {
                $('#hover_msg').show();
            }); 
        }
    });
});

//Aux pop up method
$(window).on('load',function () {
    $('.hover_msg').click(function(){
        $('.hover_msg').hide();
    });
});

//last polygon drawn
map.on('pm:create', function(e){
    var geoJSON = e.layer.toGeoJSON();
    var center = e.layer.getBounds().getCenter();
    var area = getArea(e.layer.getLatLngs()[0])
    geoJSON['center'] = [center['lat'],center['lng']];
    geoJSON['area'] = area;
    geoJSON['data'] = window.geoData;
    window.polygon = e.layer;
    window.geoJson = geoJSON;
    if(window.geoJson['area'] > 1500000){
        alert('too large polygon');
        remove();
    }
});

//--------------------------------------------------------------------------------------------------------------------------------------------
//Search-box

var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
var ErsiProvider = window.GeoSearch.EsriProvider;

var provider = new OpenStreetMapProvider();
var providerErsi = new ErsiProvider();

var searchControl = new GeoSearchControl({
    provider: providerErsi,
    searchLabel: 'Introduce tu dirección',
    style: 'bar',
  });

map.addControl(searchControl);

//sacar search-box
document.getElementById('findbox').appendChild(
    //style: bar
    document.querySelector('.leaflet-control-container > .leaflet-geosearch-bar')
    //style: button | default
    //document.querySelector('.geosearch')
);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//--------------------------------------------------------------------------------------------------------------------------------------------
//funciones steps

map.on('geosearch/showlocation', function(e) {
    passData(e.location.y, e.location.x, e.location.label);
    
});

function GetCoordinates(lat,lon){
    map.setView([lat,lon],17,{
        animate: true,
    });
    passData(lat,lon,-1);
}

function createMarker(lat, lon){
    L.marker([lat, lon], { pmIgnore: false }).addTo(map);
}

function passData(lat, lon, location){
    if(location != -1){
        location = location.normalize("NFD").replace(/\p{Diacritic}/gu, "")
    }
    var data = [lat,lon, location];
    window.geoData = data;
    clearLayer();
    createMarker(lat,lon);
    map.pm.Toolbar.setButtonDisabled('drawPolygon', false);
    document.getElementById('step-2').click();
}

function remove(){
    if(window.polygon !== undefined){
        map.removeLayer(window.polygon);
        window.geoJson = undefined;
    }
}

function clearLayer(){
    for(; Object.keys(map._layers).length > 1;) {
        if(map._layers)
        map.removeLayer(map._layers[Object.keys(map._layers)[1]]);
      }
}

function getArea(latLngs){
    var pointsCount = latLngs.length,
				area = 0.0,
				d2r = Math.PI / 180,
				p1, p2;

			if (pointsCount > 2) {
				for (var i = 0; i < pointsCount; i++) {
					p1 = latLngs[i];
					p2 = latLngs[(i + 1) % pointsCount];
					area += ((p2.lng - p1.lng) * d2r) *
						(2 + Math.sin(p1.lat * d2r) + Math.sin(p2.lat * d2r));
				}
				area = area * 6378137.0 * 6378137.0 / 2.0;
			}

			return Math.abs(area);
}

function getParcel(){
    if(window.geoData == undefined){
        jQuery(function($) {
            $('#hover_msg2').show();
        }); 
        document.getElementById('step-1').click();
    }else if(window.geoJson == undefined){
        alert("draw the polygon");
    }else{
        $.ajax({
            url: "polygon", 
            method: "POST",
            data : JSON.stringify({Data: window.geoJson}),
            contentType: 'application/json',
            success: function (returned_data) { 
                data = JSON.parse(returned_data);
                window.geoJson = data;
            },
            error: function () {
                alert('An error occured');
            }
        });
        document.getElementById('step-3').click();
    }
}

function params(){
    form = document.getElementById('params');
        params = []
        for (var i = 0; i < form.length; i++) {
            if(form[i].checked){
                params.push(form[i].name)
            }
        }
    if(params.length == 0){
        alert("please select parameters");
    }else{
        window.geoJson['params'] = params;
        document.getElementById('l-confirm').remove();
        var cbconfirm = document.getElementById('cb-confirm');
        var newP = document.createElement('p');
        var text = 'Latitude: ' + window.geoJson["data"][0] + '\nLongitude: ' + window.geoJson["data"][0];
        if (window.geoJson['data'][2] != -1){
            text += '\nname: ' + window.geoJson['data'][2];
        }
        text += '\nParams:';
        console.log(params);
        for (var i = 0; i < params.length; i++) {
                text += '\n' + params[i]
        }
        var NodeT = document.createTextNode(text)
        newP.style.whiteSpace = 'pre';
        newP.appendChild(NodeT)
        cbconfirm.prepend(newP)
        document.getElementById('step-4').click();
    }
}

function finish(){
    if(window.geoData == undefined){
        jQuery(function($) {
            $('#hover_msg2').show();
        }); 
        document.getElementById('step-1').click();
    }else if(window.geoJson == undefined){
        jQuery(function($) {
            $('#hover_msg2').show();
        }); 
        document.getElementById('step-2').click();
    }else if(window.geoJson['params'] == undefined){
        alert("please select parameters");
        document.getElementById('step-3').click();
    }else{
        $.ajax({
            url: "report", 
            headers: {'X-CSRFToken': csrftoken},
            method: "POST",
            data : JSON.stringify({Data: window.geoJson}),
            contentType: 'application/json',
            success: function () { 
                alert('Data saved')
            },
            error: function () {
                alert('An error occured');
            }
        });
        
    }
}

function test(){
    $.ajax({
        url: "test", 
        method: "POST",
        success: function (returned_data) { 
            data = JSON.stringify(returned_data)
            console.log(data);
        },
        error: function () {
            alert('An error occured');
        }
    });
}