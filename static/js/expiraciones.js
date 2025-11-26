(function(){
  function fmt(dateStr){
    // Convierte YYYY-MM-DD a DD/MM/YYYY
    const parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    return `${parts[2]}/${parts[1]}/${parts[0]}`;
  }

  function renderList(items, listId, extraWrapId, extraListId, toggleBtnId, emptyMessage){
    const list = document.getElementById(listId);
    const extraWrap = document.getElementById(extraWrapId);
    const extraList = document.getElementById(extraListId);
    const toggleBtn = document.getElementById(toggleBtnId);

    if (!list || !extraWrap || !extraList || !toggleBtn) return;

    if (!items || items.length === 0){
      list.innerHTML = `<li>${emptyMessage}</li>`;
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
      toggleBtn.textContent = 'Ver más';
      toggleBtn.onclick = function(){
        open = !open;
        extraWrap.style.display = open ? 'block' : 'none';
      };
    } else {
      extraWrap.style.display = 'none';
      toggleBtn.style.display = 'none';
    }
  }

  async function loadVencimientos(url, listId, extraWrapId, extraListId, toggleBtnId, dias){
    try {
      const res = await fetch(url, {credentials: 'same-origin'});
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      renderList(
        data.items || [], 
        listId, 
        extraWrapId, 
        extraListId, 
        toggleBtnId, 
        `No hay productos por vencer en ${dias} días.`
      );
    } catch (err){
      const list = document.getElementById(listId);
      if (list) list.innerHTML = `<li>Error cargando vencimientos: ${err.message}</li>`;
    }
  }

  document.addEventListener('DOMContentLoaded', function(){
    // Cargar vencimientos de 7 días
    loadVencimientos(
      '/api/proximos-vencimientos/',
      'vencimientos-list',
      'vencimientos-extra',
      'vencimientos-extra-list',
      'vencimientos-toggle',
      7
    );

    // Cargar vencimientos de 14 días
    loadVencimientos(
      '/api/proximos-vencimientos-14/',
      'vencimientos-14-list',
      'vencimientos-14-extra',
      'vencimientos-14-extra-list',
      'vencimientos-14-toggle',
      14
    );

    // Cargar vencimientos de 30 días
    loadVencimientos(
      '/api/proximos-vencimientos-30/',
      'vencimientos-30-list',
      'vencimientos-30-extra',
      'vencimientos-30-extra-list',
      'vencimientos-30-toggle',
      30
    );
  });
})();