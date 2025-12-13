/**
 * Dibuja un gráfico de tipo "velocímetro" (gauge) usando D3.js.
 *
 * @param {string} containerSelector - El selector CSS para el div contenedor donde se dibujará el gráfico.
 * @param {number} value - El valor actual a mostrar en el gráfico.
 * @param {number} maxValue - El valor máximo posible (el 100% del velocímetro).
 * @param {string} label - La etiqueta que se mostrará debajo del valor numérico.
 */
function drawGauge(containerSelector, value, maxValue, label) {
    // Limpiar el contenedor por si ya existía un gráfico previo
    d3.select(containerSelector).select("svg").remove();

    // --- Configuración del gráfico ---
    const container = d3.select(containerSelector);
    const width = 200; // Ancho del SVG
    const height = 140; // Alto del SVG, ajustado para medio círculo
    const margin = { top: 0, right: 20, bottom: 30, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // --- Creación del SVG ---
    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height - margin.bottom})`); // Centrado y en la base

    // --- Escala y Arcos ---
    const scale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([-Math.PI / 2, Math.PI / 2]); // Rango para medio círculo

    const arc = d3.arc()
        .innerRadius(80)
        .outerRadius(100)
        .startAngle((d) => scale(d.start))
        .endAngle((d) => scale(d.end))
        .cornerRadius(5);

    // --- Dibujo de los Arcos ---
    // 1. Arco de fondo (el 100%)
    svg.append("path")
        .datum({ start: 0, end: maxValue })
        .style("fill", "#eee") // Color gris claro para el fondo
        .attr("d", arc);

    // 2. Arco del valor actual
    svg.append("path")
        .datum({ start: 0, end: value })
        .style("fill", "#6495ED") // Color azul cornflower
        .attr("d", arc);

    // --- Textos ---
    // 1. Texto del valor (el número grande)
    svg.append("text")
        .attr("class", "gauge-value")
        .attr("text-anchor", "middle")
        .attr("dy", "1.0em") // Posición vertical
        .style("font-size", "1.5em")
        .style("font-weight", "bold")
        .text(`$${(value / 1000000).toFixed(1)}M`); // Formateado a millones

    // 2. Texto de la etiqueta (debajo del valor)
    svg.append("text")
        .attr("class", "gauge-label")
        .attr("text-anchor", "middle")
        .attr("dy", "-0.8em") // Posición vertical
        .style("font-size", "1em")
        .text(label);
}

/**
 * Inicializa un gráfico de velocímetro, obteniendo los datos de una URL.
 *
 * @param {string} containerSelector - El selector CSS para el div contenedor.
 * @param {string} dataUrl - La URL de la API de donde se obtendrán los datos.
 * @param {number} maxValue - El valor máximo para la escala del gráfico.
 * @param {string} label - La etiqueta para el gráfico.
 */
function initGaugeChart(containerSelector, dataUrl, maxValue, label) {
    fetch(dataUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la red: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Una vez que tenemos los datos, llamamos a la función que dibuja el gráfico.
            drawGauge(containerSelector, data.perdida_total, maxValue, label);
        })
        .catch(error => {
            console.error(`Error al inicializar el gráfico para ${containerSelector}:`, error);
            // Opcional: Mostrar un mensaje de error en el contenedor
            d3.select(containerSelector).html(`<p style="color: red; text-align: center;">No se pudo cargar el gráfico.</p>`);
        });
}