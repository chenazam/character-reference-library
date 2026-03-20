# Dennis

<div class="character-header">

--8<-- "snippets/galleries/dennis/hero.md"

<div class="character-overview-text">

<p>Dennis is a medium-height man with a soft, naturally untrained physique and a clearly hip-dominant silhouette. Most of his body mass sits in the abdomen, hips, glutes, and thighs, while his shoulders and upper body appear lighter by comparison, giving him rounded lower-body contours rather than an athletic V-shape.</p>

<p>His face is gentle and approachable, with a soft round structure, freckles across the nose, and rectangular glasses that reinforce his everyday appearance. Dennis reads as a calm, grounded person with a quiet presence — someone ordinary, thoughtful, and quietly warm rather than physically imposing.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 175 cm / 5&#x27;9&quot;</li>
  <li><strong>Build:</strong> soft heavy</li>
  <li><strong>Silhouette:</strong> hip dominant</li>
  <li><strong>Face:</strong> soft round and soft jawline</li>
  <li><strong>Hair:</strong> short dark hair with natural parting and light texture</li>
  <li><strong>Eyes:</strong> medium eyes behind rectangular glasses with a calm neutral gaze</li>
  <li><strong>Style:</strong> domestic soft, casual, and minimal</li>
  <li><strong>Palette:</strong> navy and neutral</li>
  <li><strong>Materials:</strong> cotton and wool</li>
  <li><strong>Expression:</strong> soft neutral and gentle</li>
  <li><strong>Movement:</strong> relaxed natural</li>
  <li><strong>Presence:</strong> grounded</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--soft_curvy height-lineup__placeholder--glute_emphasis height-lineup__placeholder--dense" style="height: 97.22%"></div>
    </div>
    <div class="height-lineup__label">Dennis</div>
    <div class="height-lineup__meta">175 cm / 5'9"</div>
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

--8<-- "snippets/galleries/dennis/identity.md"

---

## Body

--8<-- "snippets/galleries/dennis/body.md"

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
