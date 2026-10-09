(() => {
  const styles = ['academic', 'discovery', 'editorial'];
  const styleTabs = [...document.querySelectorAll('[data-style][role="tab"]')];
  const applyStyle = (style, updateUrl = false) => {
    if (!styles.includes(style)) style = 'academic';
    document.documentElement.dataset.style = style;
    styleTabs.forEach(tab => {
      const selected = tab.dataset.style === style;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    document.querySelector('#main')?.setAttribute('aria-labelledby', `style-${style}`);
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', {
      academic: '#f7f6f2', discovery: '#101d2a', editorial: '#ffffff'
    }[style]);
    try { localStorage.setItem('tang-lab-style', style); } catch (_) {}
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set('style', style);
      history.replaceState(null, '', url);
    }
    document.querySelectorAll('a[href]').forEach(link => {
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin) return;
      url.searchParams.set('style', style);
      link.href = url.href;
    });
  };
  applyStyle(document.documentElement.dataset.style);
  styleTabs.forEach((tab, index) => {
    tab.addEventListener('click', () => applyStyle(tab.dataset.style, true));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % styleTabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + styleTabs.length) % styleTabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = styleTabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      styleTabs[next].focus();
      applyStyle(styleTabs[next].dataset.style, true);
    });
  });
  window.addEventListener('popstate', () => {
    applyStyle(new URLSearchParams(location.search).get('style') || 'academic');
  });

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
