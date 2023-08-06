
    function showSeasonContent() {
    var selectedSeasonId = document.getElementById("seasonsMenu").value;
    var seasonContent = document.getElementById("seasonContent");

    // Perform an AJAX request to get the teams for the selected season
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
    seasonContent.innerHTML = this.responseText;
}
};
    var competitionId = {{competition.id}};
    var url = "/competitions/" + competitionId + "/seasons/" + selectedSeasonId + "/";
    xhttp.open("GET", url, true);
    xhttp.send();
}

    // Show the content of the first option when the page loads
    window.onload = function () {
    showSeasonContent();
};


function sortTeamsInGroups() {
    var idCompetencia = {
    {
        competition.id
    }
}
    ;
    var idSeason = {
    {
        season.id
    }
}
    ;
    var url = `/competitions/${idCompetencia}/seasons/${idSeason}/draw_groups/`;
    console.log(url); // Agregar un console.log para verificar la URL
    //window.location.href = url;
}
