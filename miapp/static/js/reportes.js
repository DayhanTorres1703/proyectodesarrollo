$(function() {
    //Definir intervalo
    //en el intervalo hacer peticiones get ajax a la vista leerReportes
    //recargar el div de mensajes
    setInterval(function(){
        $.get("/leer_Respaldo/", function(data){
            $("#reportes").html("");
            $.each(data, function(i, reporte){
                // Construir la estructura de la tabla
                var htmlRow = "<tr>";
                htmlRow += "<td>" + reporte.fields.hora + "</td>";
                htmlRow += "<td>" + reporte.fields.estado + "</td>";
                htmlRow += "<td>" + reporte.fields.nombre + "</td>";
                htmlRow += "</tr>";

                // Agregar la fila a la tabla
                $("#reportes").append(htmlRow);
            });
        });
    }, 1000);
});
