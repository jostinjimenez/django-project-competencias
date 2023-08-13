const alertPlaceholder = document.getElementById('liveAlertPlaceholder');

const appendAlert = (message, type) => {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('');

    alertPlaceholder.appendChild(wrapper);

    // Agregamos la clase 'fade-out' después de agregar el mensaje de alerta
    wrapper.firstChild.classList.add('fade-out');

    // Después de 3 segundos, eliminamos la alerta del DOM
    setTimeout(() => {
        wrapper.remove();
    }, 3000);
};

const alertTrigger = document.getElementById('liveAlertBtn');
if (alertTrigger) {
    alertTrigger.addEventListener('click', () => {
        appendAlert('La competicion ha sido activada', 'success');
    });
}

function searchTableTeam() {
    var input, filter, found, table, tr, td, i, j;
    input = document.getElementById("search-table");
    filter = input.value.toUpperCase();
    table = document.getElementById("team_table");
    tr = table.getElementsByTagName("tr");
    var noResultsMessage = document.getElementById("no-results-message");
    var anyResults = false;

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
                found = true;
                anyResults = true;
                break;
            }
        }
        if (found) {
            tr[i].style.display = "";
            found = false;
        } else {
            tr[i].style.display = "none";
        }
    }

    // Mostrar u ocultar el mensaje de "no se encontraron registros coincidentes"
    if (anyResults) {
        noResultsMessage.style.display = "none";
    } else {
        noResultsMessage.style.display = "block";
    }
}

