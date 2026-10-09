(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  const closeMenu = () => {
    if (!toggle || !nav) return;
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
  };
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    nav.classList.toggle('is-open', open);
  });
  nav?.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });

  const search = document.querySelector('#publication-search');
  if (!search) return;
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const publications = [...document.querySelectorAll('.publication')];
  const resultCount = document.querySelector('#result-count');
  const empty = document.querySelector('#no-results');
  let topic = 'All research';
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    publications.forEach(publication => {
      const visible = (topic === 'All research' || publication.dataset.topic === topic)
        && publication.dataset.search.includes(query);
      publication.hidden = !visible;
      if (visible) count++;
    });
    resultCount.textContent = `${count} selected publication${count === 1 ? '' : 's'}`;
    empty.hidden = count !== 0;
  };
  const setFilter = value => {
    topic = value;
    buttons.forEach(button => {
      const active = button.dataset.filter === value;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    update();
  };
  search.addEventListener('input', update);
  search.closest('form').addEventListener('submit', event => event.preventDefault());
  buttons.forEach(button => button.addEventListener('click', () => setFilter(button.dataset.filter)));
  document.querySelector('#reset-filters')?.addEventListener('click', () => {
    search.value = '';
    setFilter('All research');
    search.focus();
  });
})();
