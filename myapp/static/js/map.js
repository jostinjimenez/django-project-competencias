function loadMapScenario() {
    map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
        credentials: 'ApzrK8-qiiRRdCt-zCJCBU42D-OCpYnOW-Yu47cE30jPPlILtWr52Z_ySM0wErJA'
    });

    // Agrega un manejador de eventos al mapa para el evento click
    Microsoft.Maps.Events.addHandler(map, 'click', function (e) {
        // Verifica que el tipo de objetivo sea el mapa
        if (e.targetType == 'map') {
            // Obtiene la ubicación del punto donde se hizo clic
            var point = new Microsoft.Maps.Point(e.getX(), e.getY());
            var location = e.target.tryPixelToLocation(point);

            // Crea un marcador rojo con la ubicación
            var pushpin = new Microsoft.Maps.Pushpin(location, {
                color: 'red'
            });

            // Agrega el marcador al mapa
            map.entities.push(pushpin);
        }
    });
}