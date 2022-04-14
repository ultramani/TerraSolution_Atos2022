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
    drawRectangle: false,
    // drawPolygon: false,
    drawCircleMarker: false,
    editMode: false,
    dragMode: false,
    cutPolygon: false,
    rotateMode: false,

}); 

//Limit side of polygon
map.on('pm:drawstart', function(e) {
    var nVertex = 0;
    e.workingLayer.on('pm:vertexadded', function(e) {
        nVertex += 1;
        if(nVertex >10){
            map.pm.Draw.Polygon._removeLastVertex();
            nVertex -= 1;
            alert('Max 10 sides');
        }
    });
});

//last polygon drawn
map.on('pm:create', function(e){
    window.geoJson = e.layer.toGeoJSON();
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

function passData(lat, lon, location){
    var data = [lat,lon];
    if (location!=-1){
        data.push(location);
    }
    window.geoData = data;
    clearLayer();
    L.marker([lat, lon], { pmIgnore: false }).addTo(map);
    document.getElementById('step-2').click();
}

function clearLayer(){
    for(; Object.keys(map._layers).length > 1;) {
        map.removeLayer(map._layers[Object.keys(map._layers)[1]]);
      }
}

function getParcel(){
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
    document.getElementById('step-3').click();
}

function finish(){
    form = document.getElementById('params');
    params = []
    for (var i = 0; i < form.length; i++) {
        if(form[i].checked){
            params.push(form[i].name)
        }
    }
    data =JSON.parse(JSON.stringify(window.geoData));
    data.push(params);
    console.log(data);
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