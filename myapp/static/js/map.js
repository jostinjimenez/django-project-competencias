function loadMapScenario() {
    var map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
        credentials: 'ApzrK8-qiiRRdCt-zCJCBU42D-OCpYnOW-Yu47cE30jPPlILtWr52Z_ySM0wErJA'
    });
}

Microsoft.Maps.Events.addHandler(map, 'click', function (e) {
    if (e.targetType == 'map') {
        var point = new Microsoft.Maps.Point(e.getX(), e.getY());
        var location = e.target.tryPixelToLocation(point);
        document.getElementById('geolocation').value = location.latitude + ',' + location.longitude;
    }
});
