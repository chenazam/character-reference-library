# Noel

<div class="character-header">

--8<-- "snippets/galleries/noel/hero.md"

<div class="character-overview-text">

<p>fashion-aware, playful, luxury-indulged young man with soft masculine beauty, model-like proportions, and a bratty-confident charm He is characterized by a oval; defined jawline; short to medium dark brown hair with natural wave, airy volume, and slight curl; soft but lively eyes with a playful, self-aware gaze. His style centers on athletic luxury, with influences from luxury, streetwear, and romantic. He moves with relaxed natural and projects a expansive.</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 180 cm / 5&#x27;11&quot;</li>
  <li><strong>Build:</strong> light athletic</li>
  <li><strong>Silhouette:</strong> elongated frame</li>
  <li><strong>Face:</strong> oval and defined jawline</li>
  <li><strong>Hair:</strong> short to medium dark brown hair with natural wave, airy volume, and slight curl</li>
  <li><strong>Eyes:</strong> soft but lively eyes with a playful, self-aware gaze</li>
  <li><strong>Style:</strong> athletic luxury, luxury, streetwear, and romantic</li>
  <li><strong>Palette:</strong> black, cream, and white</li>
  <li><strong>Materials:</strong> cotton, leather, and silk</li>
  <li><strong>Expression:</strong> confident neutral and open warm</li>
  <li><strong>Movement:</strong> relaxed natural</li>
  <li><strong>Presence:</strong> expansive</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--reference" style="height: 100.00%"></div>
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--elongated" style="height: 100.00%"></div>
    </div>
    <div class="height-lineup__label">Noel</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
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

--8<-- "snippets/galleries/noel/identity.md"

---

## Body

--8<-- "snippets/galleries/noel/body.md"

---

## Style

--8<-- "snippets/galleries/noel/style.md"

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
