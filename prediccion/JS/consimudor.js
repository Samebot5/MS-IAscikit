// Función asíncrona que realizará la verificación llamando a la API
/*async function verificar() {

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
}*/
// Función para cargar el Dashboard Inteligente
async function cargarDashboardIA() {
    try {
        // Llamamos al endpoint que acabamos de crear en urls.py
        const response = await fetch('/api/dashboard-ia/');
        const data = await response.json();

        console.log("Cerebro IA responde:", data);

        // 1. Mostrar Alertas de Stock (Punto 4)
        const alertasDiv = document.getElementById('alertas-stock');
        alertasDiv.innerHTML = ""; // Limpiar

        data.alertas_inventario.forEach(alerta => {
            // Crear una tarjeta roja si es urgente
            alertasDiv.innerHTML += `
                <div class="alert alert-danger">
                    <strong>¡OJO!</strong> El ${alerta.producto} se acaba en ${alerta.dias_restantes} días.
                    <br>Sugiero comprar: ${alerta.sugerencia_compra} unidades.
                </div>
            `;
        });

        // 2. Mostrar Sugerencias de Precio (Punto 3)
        data.sugerencias_precio.forEach(sugerencia => {
            console.log(`IA sugiere: ${sugerencia.accion} el precio de ${sugerencia.producto}`);
        });

    } catch (error) {
        console.error('Error conectando con la IA:', error);
    }
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', cargarDashboardIA);
