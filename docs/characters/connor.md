# Connor

<div class="character-header">

--8<-- "snippets/galleries/connor/hero.md"

<div class="character-overview-text">

<p>Connor is a slim young man with a soft athletic build and a gentle, approachable presence. His physique is lightly trained, with a natural runner’s silhouette that emphasizes the lower body—his thighs and glutes are subtly more developed than his upper body, while his shoulders and torso remain lighter and less defined. This creates a soft, slightly inward silhouette that reads as relaxed and non-threatening rather than physically assertive.</p>

<p>His face is youthful and soft-featured, with a rounded structure, blue-grey eyes, and short medium-brown hair with a natural, slightly tousled texture. Subtle freckles across his nose and cheeks enhance his boyish appearance. Connor’s overall presence is warm, calm, and slightly shy, with an occasional absentminded quality that makes him feel gentle and emotionally open.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 175 cm / 5&#x27;9&quot;</li>
  <li><strong>Build:</strong> runner build</li>
  <li><strong>Silhouette:</strong> leg dominant</li>
  <li><strong>Face:</strong> soft round and soft jawline</li>
  <li><strong>Hair:</strong> short medium-brown hair with soft natural texture and slight curl</li>
  <li><strong>Eyes:</strong> blue-grey eyes with a gentle, slightly absentminded expression</li>
  <li><strong>Style:</strong> [&#x27;domestic soft&#x27;] and romantic</li>
  <li><strong>Palette:</strong> beige and light blue</li>
  <li><strong>Materials:</strong> cotton and linen</li>
  <li><strong>Expression:</strong> soft neutral and gentle</li>
  <li><strong>Movement:</strong> relaxed natural</li>
  <li><strong>Presence:</strong> compact presence</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_leg_dominant height-lineup__placeholder--glute_emphasis" style="height: 97.22%"></div>
    </div>
    <div class="height-lineup__label">Connor</div>
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

--8<-- "snippets/galleries/connor/identity.md"

---

## Body

--8<-- "snippets/galleries/connor/body.md"

---

## Style

--8<-- "snippets/galleries/connor/style.md"

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
