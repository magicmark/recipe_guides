(() => {
  const key = 'dinner-sorted:' + document.body.dataset.week;
  const boxes = [...document.querySelectorAll('.shopping-content input[type=checkbox]')];
  let saved = [];
  try { const parsed = JSON.parse(localStorage.getItem(key) || '[]'); if (Array.isArray(parsed)) saved = parsed; } catch (_) {}
  boxes.forEach((box, i) => { box.checked = saved.includes(i); });
  const update = () => {
    document.querySelector('#shop-count').textContent = `${boxes.filter(b => b.checked).length} / ${boxes.length} in the cart`;
    try { localStorage.setItem(key, JSON.stringify(boxes.flatMap((b,i) => b.checked ? [i] : []))); } catch (_) {}
  };
  boxes.forEach(box => box.addEventListener('change', update));
  document.querySelector('.shop-controls').hidden = false;
  document.querySelector('#reset-list').addEventListener('click', () => { boxes.forEach(b => b.checked = false); update(); });
  update();
  document.querySelector('#week-select').addEventListener('change', e => { location.href = e.target.value; });
  const openRecipe = () => {
    if (!/^#recipe-\d+$/.test(location.hash)) return;
    const recipe = document.querySelector(location.hash);
    if (recipe) { recipe.open = true; recipe.scrollIntoView({block:'start'}); }
  };
  window.addEventListener('hashchange', openRecipe);
  document.querySelectorAll('.meal').forEach(a => a.addEventListener('click', () => { document.querySelector(a.hash).open = true; }));
  openRecipe();
  const printButton = document.querySelector('.print-button');
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
  let opened = [];
  window.addEventListener('beforeprint', () => { opened = [...document.querySelectorAll('details')].map(d => d.open); document.querySelectorAll('details').forEach(d => d.open = true); });
  window.addEventListener('afterprint', () => document.querySelectorAll('details').forEach((d,i) => d.open = opened[i]));
})();
