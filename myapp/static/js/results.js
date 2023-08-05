// results.js
$(document).ready(function () {
    // Capturar el evento de clic en los enlaces del menú desplegable
    $('.dropdown-item').on('click', function (e) {
        e.preventDefault();

        // Obtener el ID de la temporada seleccionada desde el atributo data-id
        var seasonId = $(this).data('id');

        // Realizar la petición AJAX para obtener la información de la temporada seleccionada
        $.ajax({
            type: 'GET',
            url: '/get_season_info/' + seasonId + '/',  // Reemplaza con la URL correcta de la vista para obtener la información de la temporada
            success: function (response) {
                // Actualizar el contenido de la sección 'season-info' con la información de la temporada
                $('#season-info').html(response);
            },
            error: function () {
                alert('Error al obtener la información de la temporada.');
            }
        });
    });
});
