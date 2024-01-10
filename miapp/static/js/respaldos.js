$(function(){
    $("#enviarRespaldo").click(function(){
        $.post("/respaldar_servidor/", {ipOrigen: $("#servidorOrigen").val(), ipDestino: $("#servidorDestino").val(), dirOrigen: $("#directorioOrigen").val(), dirDestino: $("#directorioDestino").val(), cron: $("#periodicidad").val()}),
        function(data, status){
            if(status == "success"){
                if(data.status != "OK"){
                    alert("No se lograron mandar los datos");
                }
            }
        }
    });
});