// ================================================================
// =                                                              =
// =        JAVASCRIPT PARA MENÚ DE USUARIO                       =
// =                                                              =
// ================================================================
//
// Maneja el menú desplegable del usuario en el header

document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('userMenuButton');
  const menu = document.getElementById('userMenu');
  if (!btn || !menu) return;

  function hide(){
    menu.hidden = true;
    menu.classList.remove('open');
    menu.setAttribute('aria-hidden','true');
  }

  function toggle(){
    const willOpen = menu.hidden;
    menu.hidden = !willOpen;
    menu.classList.toggle('open', willOpen);
    menu.setAttribute('aria-hidden', String(!willOpen));
  }

  btn.addEventListener('click', function(e){ e.stopPropagation(); toggle(); });
  document.addEventListener('click', hide);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') hide(); });
});

