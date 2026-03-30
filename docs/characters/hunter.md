# Hunter

<div class="character-header">

--8<-- "snippets/galleries/hunter/hero.md"

<div class="character-overview-text">

<p>A grounded, physically dense man with quiet dominance and controlled presence. He is characterized by a square oval; strong defined; dark, dense, controlled, slightly wavy; deep-set eyes with a steady, assessing gaze. His style centers on modern minimal masculine, with influences from athletic clean, quiet luxury, and utilitarian refined. He moves with deliberate economical and projects a center of gravity.</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 188 cm / 6&#x27;2&quot;</li>
  <li><strong>Build:</strong> athletic powerful</li>
  <li><strong>Silhouette:</strong> broad upper body</li>
  <li><strong>Face:</strong> square oval and strong defined</li>
  <li><strong>Hair:</strong> dark, dense, controlled, slightly wavy</li>
  <li><strong>Eyes:</strong> deep-set eyes with a steady, assessing gaze</li>
  <li><strong>Style:</strong> modern minimal masculine, athletic clean, quiet luxury, and utilitarian refined</li>
  <li><strong>Palette:</strong> black, charcoal, and navy</li>
  <li><strong>Materials:</strong> cotton, wool, and leather</li>
  <li><strong>Expression:</strong> neutral controlled and low variance high control</li>
  <li><strong>Movement:</strong> deliberate economical</li>
  <li><strong>Presence:</strong> center of gravity</li>
</ul>
</div>

</div>

</div>

---

## Height Context

<div class="height-lineup height-lineup--character-context">
  <div class="height-lineup__baseline" aria-hidden="true"></div>

  <div class="height-lineup__figure height-lineup__figure--ref">
    <div class="height-lineup__stage">
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--reference" style="height: 95.74%"></div>
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--elongated" style="height: 100.00%"></div>
    </div>
    <div class="height-lineup__label">Hunter</div>
    <div class="height-lineup__meta">188 cm / 6'2"</div>
  </div>
</div>



---

<div class="gallery-version-toggle" role="group" aria-label="Asset version display">
  <label class="gallery-version-toggle__label">
    <input class="gallery-version-toggle__input" type="checkbox" id="show-all-versions-toggle">
    <span>Show all versions</span>
  </label>
</div>

## Identity

--8<-- "snippets/galleries/hunter/identity.md"

---

## Body

--8<-- "snippets/galleries/hunter/body.md"

---

## Style

--8<-- "snippets/galleries/hunter/style.md"

---

<script>
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('show-all-versions-toggle');
  if (!toggle) return;
  var root = document.documentElement;
  var storageKey = 'character-gallery-version-mode';
  try {
    if (window.localStorage && localStorage.getItem(storageKey) === 'all') {
      toggle.checked = true;
    }
  } catch (error) {}

  function applyMode() {
    var mode = toggle.checked ? 'all' : 'latest';
    root.setAttribute('data-gallery-versions', mode);
    try {
      if (window.localStorage) {
        localStorage.setItem(storageKey, mode);
      }
    } catch (error) {}
  }

  toggle.addEventListener('change', applyMode);
  applyMode();
});
</script>
