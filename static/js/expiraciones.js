(function(){
  function fmt(dateStr){
    // Convierte YYYY-MM-DD a DD/MM/YYYY
    const parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    return `${parts[2]}/${parts[1]}/${parts[0]}`;
  }

  function render(items){
    const list = document.getElementById('vencimientos-list');
    const extraWrap = document.getElementById('vencimientos-extra');
    const extraList = document.getElementById('vencimientos-extra-list');
    const toggleBtn = document.getElementById('vencimientos-toggle');

    if (!list || !extraWrap || !extraList || !toggleBtn) return;

    if (!items || items.length === 0){
      list.innerHTML = '<li>No hay productos por vencer en 7 días.</li>';
      toggleBtn.style.display = 'none';
      return;
    }

    const first = items.slice(0, 5);
    const rest = items.slice(5);

    list.innerHTML = first.map(it => `<li>${it.nombre} — ${fmt(it.caducidad)}</li>`).join('');

    if (rest.length > 0){
      extraList.innerHTML = rest.map(it => `<li>${it.nombre} — ${fmt(it.caducidad)}</li>`).join('');
      toggleBtn.style.display = 'inline-block';
      let open = false;
      toggleBtn.textContent = 'Ver más'; // mantener siempre "Ver más"
      toggleBtn.onclick = function(){
        open = !open;
        extraWrap.style.display = open ? 'block' : 'none';
      };
    } else {
      extraWrap.style.display = 'none';
      toggleBtn.style.display = 'none';
    }
  }

  async function load(){
    try {
      const res = await fetch('/api/proximos-vencimientos/', {credentials: 'same-origin'});
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(data.items || []);
    } catch (err){
      const list = document.getElementById('vencimientos-list');
      if (list) list.innerHTML = `<li>Error cargando vencimientos: ${err.message}</li>`;
    }
  }

  document.addEventListener('DOMContentLoaded', load);
})();