# Aaron

<div class="character-header">

--8<-- "snippets/galleries/aaron/hero.md"

<div class="character-overview-text">

<p>1–2 paragraphs of natural prose describing the character’s overall appearance, silhouette, presence, and vibe.  
This text is used directly for the character page overview.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 178 cm / 5&#x27;10&quot;</li>
  <li><strong>Build:</strong> light athletic</li>
  <li><strong>Silhouette:</strong> balanced frame</li>
  <li><strong>Face:</strong> oval and defined jawline</li>
  <li><strong>Hair:</strong> short to medium-length hair with natural volume and lightly tousled structure</li>
  <li><strong>Eyes:</strong> clear and expressive with a slightly open, attentive gaze</li>
  <li><strong>Style:</strong> playful athletic and athletic</li>
  <li><strong>Palette:</strong> black and orange</li>
  <li><strong>Materials:</strong> cotton and linen</li>
  <li><strong>Expression:</strong> confident neutral and open warm</li>
  <li><strong>Movement:</strong> restless quick</li>
  <li><strong>Presence:</strong> energetic</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--elongated" style="height: 98.89%"></div>
    </div>
    <div class="height-lineup__label">Aaron</div>
    <div class="height-lineup__meta">178 cm / 5'10"</div>
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

--8<-- "snippets/galleries/aaron/identity.md"

---

## Body

--8<-- "snippets/galleries/aaron/body.md"

---

## Style

--8<-- "snippets/galleries/aaron/style.md"

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
