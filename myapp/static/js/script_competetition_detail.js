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

