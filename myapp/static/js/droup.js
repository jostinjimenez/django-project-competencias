$(document).ready(function () {
    $("#teamList li").draggable({
        revert: "invalid",
        cursor: "move",
    });

    $("#groupList li").droppable({
        accept: "#teamList li",
        drop: function (event, ui) {
            const teamId = ui.draggable.data("team-id");
            const groupId = $(this).data("group-id");
            const teamName = ui.draggable.text();

            // Muestra el equipo asignado al grupo
            const teamInfo = `<span class="team-info">Equipo ${teamId} - ${teamName}</span>`;
            $(this).append(teamInfo);

            // Elimina la información del equipo previamente asignado
            $("#groupList .grouped")
                .not(this)
                .find(`[data-team-id="${teamId}"]`)
                .remove();
        },
    });
});
