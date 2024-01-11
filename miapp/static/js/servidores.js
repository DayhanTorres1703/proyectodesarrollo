$(function() {
    // Manejar la validación del formulario al enviar
    $("#servidorEnviar").click(function() {
        // Validar el formulario antes de enviar la solicitud
        if (validarFormulario()) {
            // Enviar la solicitud POST al servidor
            $.post("/registroServidor/", {
                nombreSer: $("#nombreServidor").val(),
                ipSer: $("#ipServidor").val(),
                usuarioSer: $("#usuarioServidor").val(),
                contraBot: $("#contrasenaBot").val()
            }, function(data, status) {
                // Manejar la respuesta del servidor si es necesario
                if (status === "success") {
                    if (data.status !== "OK") {
                        alert("No se lograron mandar los datos");
                    }
                }
            });
        }
    });

    // Función para validar el formulario
    function validarFormulario() {
        // Restablecer los mensajes de error
        $('#nombreServidorError').text('');
        $('#ipServidorError').text('');

        let esValido = true;

        // Validar nombre del servidor
        let nombreServidor = $('#nombreServidor').val().trim();
        if (nombreServidor === '') {
            $('#nombreServidorError').text('Este campo es obligatorio.');
            esValido = false;
        }

        // Validar IP del servidor
        let ipServidor = $('#ipServidor').val().trim();
        if (ipServidor === '') {
            $('#ipServidorError').text('Este campo es obligatorio.');
            esValido = false;
        } else if (!validarFormatoIP(ipServidor)) {
            $('#ipServidorError').text('Formato de IP inválido.');
            esValido = false;
        }

        return esValido;
    }

    // Función para validar el formato de una IP
    function validarFormatoIP(ip) {
        let regexIP = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
        return regexIP.test(ip);
    }
});
