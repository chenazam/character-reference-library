# Jonah

<div class="character-header">

--8<-- "snippets/galleries/jonah/hero.md"

<div class="character-overview-text">

<p>Jonah is a lean, athletic man with a dancer build, elongated proportions, expressive green eyes, and a graceful, elegant silhouette. His long limbs, balanced shoulders, and dark blonde wavy hair give him a refined visual identity that feels light, fluid, and naturally expressive.</p>

<p>His style blends playful athletic fashion with romantic and slightly provocative elements, creating a look that feels bold, youthful, and self-aware. He projects warmth, openness, and cheerful confidence, with a presence that feels affectionate, flirtatious, and emotionally bright.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 178 cm / 5&#x27;10&quot;</li>
  <li><strong>Build:</strong> lower athletic</li>
  <li><strong>Face:</strong> long oval and defined jawline</li>
  <li><strong>Hair:</strong> dark blonde medium-length wavy hair with soft side-swept volume</li>
  <li><strong>Eyes:</strong> expressive green eyes</li>
  <li><strong>Style:</strong> playful athletic, athletic, and romantic</li>
  <li><strong>Palette:</strong> black, white, pink, and red</li>
  <li><strong>Materials:</strong> cotton and mesh</li>
  <li><strong>Expression:</strong> soft neutral and open warm</li>
  <li><strong>Movement:</strong> relaxed natural</li>
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
      <div class="height-lineup__placeholder height-lineup__placeholder--athletic_leg_dominant height-lineup__placeholder--elongated" style="height: 98.89%"></div>
    </div>
    <div class="height-lineup__label">Jonah</div>
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

--8<-- "snippets/galleries/jonah/identity.md"

---

## Body

--8<-- "snippets/galleries/jonah/body.md"

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
