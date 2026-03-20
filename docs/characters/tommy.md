# Tommy

<div class="character-header">

--8<-- "snippets/galleries/tommy/hero.md"

<div class="character-overview-text">

<p>Tommy is a medium-height young man with a soft, slightly curvy natural build and a gentle, youthful presence. His fuller hips, glutes, and thighs give him a compact leg-dominant silhouette, while his soft facial structure and light brown hair make his overall appearance feel warm and approachable.</p>

<p>His aesthetic is cozy, casual, and softly romantic, favoring comfortable clothing and a more tender visual tone. He reads as affectionate, emotionally open, and quietly sweet, with a softness that feels sincere rather than fragile.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 170 cm / 5&#x27;7&quot;</li>
  <li><strong>Build:</strong> soft slender</li>
  <li><strong>Silhouette:</strong> hip dominant</li>
  <li><strong>Face:</strong> soft round and soft jawline</li>
  <li><strong>Hair:</strong> light-to-medium brown hair, usually a short textured crop with slight fringe</li>
  <li><strong>Eyes:</strong> clear blue eyes with a warm, open expression</li>
  <li><strong>Style:</strong> domestic soft and romantic</li>
  <li><strong>Palette:</strong> cream and soft blue</li>
  <li><strong>Materials:</strong> cotton and linen</li>
  <li><strong>Expression:</strong> soft neutral and open warm</li>
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
      <img class="height-lineup__silhouette height-lineup__silhouette--reference" src="/assets/reference/reference_male_average_180cm_front_v1.png" alt="Reference silhouette" style="height: 100.00%;">
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/TOMMY/02_BODY/structure/tommy_silhouette_front_v1.png" alt="Tommy silhouette front" style="height: 94.44%;">
    </div>
    <div class="height-lineup__label">Tommy</div>
    <div class="height-lineup__meta">170 cm / 5'7"</div>
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

--8<-- "snippets/galleries/tommy/identity.md"

---

## Body

--8<-- "snippets/galleries/tommy/body.md"

---

## Scenes

--8<-- "snippets/galleries/tommy/scenes.md"

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
