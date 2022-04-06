//map
const map = L.map('map').setView([40, -3], 7);
map.zoomControl.setPosition('topright');
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//--------------------------------------------------------------------------------------------------------------------------------------------
//geoman
map.pm.addControls({  
    position: 'topright',  
    drawMarker: false,
    drawPolyline: false,
    drawCircle: false,
    // drawRectangle: false,
    drawPolygon: false,
    drawCircleMarker: false,
}); 

function getParcela(){
    $.ajax({
        url: "polygon", 
        method: "POST",
        data : JSON.stringify({Data: window.geoJson}),
        contentType: 'application/json',
        success: function (returned_data) { 
            data = JSON.parse(returned_data);
            console.log(data);
        },
        error: function () {
          alert('An error occured');
        }
    });

}

map.on('pm:create', function(e){
    // last polygon drawn
    window.geoJson = e.layer.toGeoJSON();
    getParcela();
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

map.on('geosearch/showlocation', function(e) {
    var data = [{'latitude': e.location.y},{'longitude': e.location.x},{'name': e.location.label}];
    $.ajax({
        url: "nasa", 
        headers: {'X-CSRFToken': csrftoken},
        method: "POST",
        data : JSON.stringify({Data: data}),
        contentType: 'application/json',
        success: function (returned_data) { 
            data = JSON.parse(returned_data);
            console.log(data);
        },
        error: function () {
          alert('An error occured');
        }
    });
});

function prueba(){
    console.log('aaa');
}

function GetCoordinates(lat,lon){
    console.log(lat,lon);
    clearLayer();
    var data = [{'latitude': lat},{'longitude': lat}];
    map.setView([lat,lon],17,{
        animate: true,
    });
    L.marker([lat, lon], { pmIgnore: false }).addTo(map);
    $.ajax({
        url: "nasa", 
        headers: {'X-CSRFToken': csrftoken},
        method: "POST",
        data : JSON.stringify({Data: data}),
        contentType: 'application/json',
        success: function (returned_data) { 
            data = JSON.parse(returned_data);
            console.log(data);
        },
        error: function () {
          alert('An error occured');
        }
    });
}

function clearLayer(){
    for(; Object.keys(map._layers).length > 1;) {
        map.removeLayer(map._layers[Object.keys(map._layers)[1]]);
      }
}