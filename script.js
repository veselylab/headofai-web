document.getElementById('yr').textContent = new Date().getFullYear();
const t = document.getElementById('navToggle'), p = document.getElementById('mobilenav');
t.addEventListener('click', () => {
  const open = p.classList.toggle('open');
  t.setAttribute('aria-expanded', open);
});
p.addEventListener('click', e => { if (e.target.tagName === 'A') { p.classList.remove('open'); t.setAttribute('aria-expanded','false'); } });
const sticky = document.getElementById('stickyCta');
const heroEl = document.querySelector('.hero'), finalEl = document.getElementById('call');
if ('IntersectionObserver' in window) {
  let heroOut = false, finalIn = false;
  const update = () => {
    const show = heroOut && !finalIn;
    sticky.classList.toggle('show', show);
    sticky.setAttribute('aria-hidden', !show);
  };
  new IntersectionObserver(e => { heroOut = !e[0].isIntersecting; update(); }, {threshold: 0.1}).observe(heroEl);
  new IntersectionObserver(e => { finalIn = e[0].isIntersecting; update(); }, {threshold: 0.1}).observe(finalEl);
}