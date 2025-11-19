async function verificar() {
    const data = {
        ventas_semana: 28,
        inventario_actual: 15
    };

    const res = await fetch("https://tu-dominio.com/api/prediccion/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const json = await res.json();
    console.log(json);
}
