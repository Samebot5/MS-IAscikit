// Función asíncrona que realizará la verificación llamando a la API
async function verificar() {

    // Datos que se enviarán al backend en formato JSON
    const data = {
        ventas_semana: 28,        // Valor de ventas de la semana
        inventario_actual: 15     // Valor del inventario actual
    };

    // Petición HTTP hacia tu API en Django
    const res = await fetch("https://tu-dominio.com/api/prediccion/", {
        method: "POST",                      // Se envía usando método POST
        headers: {
            "Content-Type": "application/json"  // Indica que se envía JSON
        },
        body: JSON.stringify(data)           // Convierte el objeto JS a JSON
    });

    // Espera la respuesta de la API en formato JSON
    const json = await res.json();

    // Imprime la respuesta en la consola del navegador
    console.log(json);
}

