# Alek

<div class="character-header">

--8<-- "snippets/galleries/alek/hero.md"

<div class="character-overview-text">

<p>1–2 paragraphs of natural prose describing the character’s overall appearance, silhouette, presence, and vibe.  
This text is used directly for the character page overview.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 195 cm / 6&#x27;5&quot;</li>
  <li><strong>Build:</strong> athletic muscular</li>
  <li><strong>Silhouette:</strong> elongated frame</li>
  <li><strong>Face:</strong> long oval and defined jawline</li>
  <li><strong>Hair:</strong> brown hair with natural volume, usually styled or tousled with controlled texture</li>
  <li><strong>Eyes:</strong> brown eyes with an intense, confident, slightly guarded gaze</li>
  <li><strong>Style:</strong> athletic luxury and streetwear</li>
  <li><strong>Palette:</strong> white, black, beige, and gray</li>
  <li><strong>Materials:</strong> linen, silk, and leather</li>
  <li><strong>Expression:</strong> confident neutral and controlled</li>
  <li><strong>Movement:</strong> deliberate precise</li>
  <li><strong>Presence:</strong> dominant presence</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_balanced height-lineup__placeholder--reference" style="height: 92.31%"></div>
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <div class="height-lineup__placeholder height-lineup__placeholder--broad_athletic height-lineup__placeholder--elongated" style="height: 100.00%"></div>
    </div>
    <div class="height-lineup__label">Alek</div>
    <div class="height-lineup__meta">195 cm / 6'5"</div>
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

--8<-- "snippets/galleries/alek/identity.md"

---

## Body

--8<-- "snippets/galleries/alek/body.md"

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
