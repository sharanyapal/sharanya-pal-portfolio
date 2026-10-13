(() => {
  'use strict';
  const collection = document.getElementById('premiereRows');
  if (!collection) return;

  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const prepareShelf = (shelf) => {
    if (shelf.dataset.carouselReady === 'true') return;
    const track = shelf.querySelector('.premiere-track');
    const controls = shelf.querySelector('.premiere-navigation');
    if (!track || !controls) return;
    shelf.dataset.carouselReady = 'true';
    const back = controls.querySelector('.premiere-back');
    const next = controls.querySelector('.premiere-next');
    const cards = [...track.querySelectorAll('.premiere-card')];
    const count = document.createElement('span');
    count.className = 'premiere-position';
    count.setAttribute('aria-live', 'off');
    controls.prepend(count);
    const progress = document.createElement('div');
    progress.className = 'premiere-scroll-progress';
    progress.setAttribute('aria-hidden', 'true');
    const thumb = document.createElement('div');
    thumb.className = 'premiere-scroll-thumb';
    progress.append(thumb);
    track.after(progress);

    function update() {
      const maxScroll = Math.max(0, track.scrollWidth - track.clientWidth);
      const current = track.scrollLeft;
      let currentIndex = 0;
      let closest = Infinity;
      cards.forEach((card, index) => {
        const difference = Math.abs(card.offsetLeft - cards[0].offsetLeft - current);
        if (difference < closest) { closest = difference; currentIndex = index; }
      });
      count.textContent = String(currentIndex + 1).padStart(2,'0') + ' / ' + String(cards.length).padStart(2,'0');
      back.disabled = current <= 2;
      next.disabled = current >= maxScroll - 2;
      const width = maxScroll ? Math.max(11, Math.min(100, 100 * track.clientWidth / track.scrollWidth)) : 100;
      thumb.style.width = width + '%';
      thumb.style.left = (maxScroll ? (100 - width) * current / maxScroll : 0) + '%';
    }

    const slide = (direction) => {
      if (!cards.length) return;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const span = cards[0].getBoundingClientRect().width + gap;
      const visible = Math.max(1, Math.floor((track.clientWidth + gap) / span));
      const maxScroll = Math.max(0, track.scrollWidth - track.clientWidth);
      const currentIndex = Math.round(track.scrollLeft / span);
      const targetIndex = Math.max(0, Math.min(cards.length - 1, currentIndex + visible * direction));
      track.scrollTo({ left: Math.min(maxScroll, targetIndex * span), behavior: reducedMotion() ? 'instant' : 'smooth' });
    };
    back.onclick = () => slide(-1);
    next.onclick = () => slide(1);
    track.addEventListener('scroll', update, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
    else window.addEventListener('resize', update, { passive: true });
    update();
  };
  const prepareAll = () => collection.querySelectorAll('.premiere-shelf').forEach(prepareShelf);
  new MutationObserver(prepareAll).observe(collection, { childList: true });
  prepareAll();

  const toggle = document.getElementById('archiveToggle');
  const archive = document.getElementById('project-archive');
  if (toggle && archive) {
    const sync = () => {
      toggle.setAttribute('aria-expanded', String(archive.open));
      toggle.textContent = archive.open ? '− HIDE EARLIER PROJECTS' : '+ EXPLORE 39 EARLIER PROJECTS';
    };
    toggle.addEventListener('click', () => {
      archive.open = !archive.open;
      sync();
      if (archive.open) archive.scrollIntoView({ behavior: reducedMotion() ? 'instant' : 'smooth', block: 'start' });
      else document.getElementById('featured-projects')?.scrollIntoView({ behavior: reducedMotion() ? 'instant' : 'smooth', block: 'start' });
    });
    archive.addEventListener('toggle', sync);
    window.addEventListener('hashchange', () => {
      if (['#project-archive', '#lab-vault', '#advanced'].includes(location.hash)) archive.open = true;
      sync();
    });
    sync();
  }
})();