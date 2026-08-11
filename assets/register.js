// Read-as toggle. The machine view is the same record, not a summary of it.
(function () {
  var btns = document.querySelectorAll('.readas button');
  if (!btns.length) return;
  function set(view) {
    document.body.classList.toggle('machine-view', view === 'machine');
    btns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.view === view));
    });
    try { history.replaceState(null, '', view === 'machine' ? '#machine' : location.pathname); } catch (e) {}
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () { set(b.dataset.view); });
  });
  if (location.hash === '#machine') set('machine');
})();
