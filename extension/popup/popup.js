document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('togglePresence');
  if (!toggle) return;

  chrome.storage.sync.get('enabled', ({ enabled }) => {
    toggle.checked = !!enabled;
  });

  toggle.addEventListener('change', () => {
    chrome.storage.sync.set({ enabled: toggle.checked });
  });
});