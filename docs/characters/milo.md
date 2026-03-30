# Milo

<div class="character-header">

--8<-- "snippets/galleries/milo/hero.md"

<div class="character-overview-text">

<p>1–2 paragraphs of natural prose describing the character’s overall appearance, silhouette, presence, and vibe.  
This text is used directly for the character page overview.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 193 cm / 6&#x27;4&quot;</li>
  <li><strong>Build:</strong> balanced athletic</li>
  <li><strong>Silhouette:</strong> balanced frame</li>
  <li><strong>Face:</strong> soft round and defined jawline</li>
  <li><strong>Hair:</strong> medium-length ginger hair with soft volume and natural, slightly tousled structure</li>
  <li><strong>Eyes:</strong> soft, steady eyes with a calm and open gaze</li>
  <li><strong>Style:</strong> domestic soft and athletic</li>
  <li><strong>Palette:</strong> green and beige</li>
  <li><strong>Materials:</strong> cotton and linen</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--reference" style="height: 93.26%"></div>
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--elongated height-lineup__placeholder--dense" style="height: 100.00%"></div>
    </div>
    <div class="height-lineup__label">Milo</div>
    <div class="height-lineup__meta">193 cm / 6'4"</div>
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

--8<-- "snippets/galleries/milo/identity.md"

---

## Body

--8<-- "snippets/galleries/milo/body.md"

---

## Style

--8<-- "snippets/galleries/milo/style.md"

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
