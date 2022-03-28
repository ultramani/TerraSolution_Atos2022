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
});